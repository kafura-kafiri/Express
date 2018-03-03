from Khorus.Choori.decorators import privileges, retrieve
from Khorus.crud.order import bp, orders
from Khorus.crud.order.design.schema import schema, obj, status as statuses
from sanic.response import json
from bson import ObjectId
from datetime import datetime, timedelta
from temp import orders as orders_cache, users as users_cache
from utils import to_list, dot_notation
from copy import deepcopy


retrieval = to_list(schema)
minus = [(feature[1][0][1:], feature[1][1], feature[0]) for feature in retrieval if '-' in feature[1][0]]
retrieval = [(feature[1][0][1:], feature[1][1], feature[0]) for feature in retrieval if '$' in feature[1][0]]


@bp.route('/', methods=['POST'])
@bp.route('/<_id>', methods=['POST'])
@privileges('dev', 'operator', 'applicator')
@retrieve(
    *['<{key}:{type}:$form:k>'.format(key=feature[0], type=feature[1]) for feature in retrieval]
)
async def _put(request, payload, _id=None, **kwargs):
    options = []
    d = deepcopy(obj)
    for pay, _type, address in minus:
        _d, key = dot_notation(d, address)
        _d[key] = payload[pay]

    if _id:
        d["crate"]["id"] = _id
    else:
        d["crate"]["id"] = str(ObjectId())

    for form, _type, address in retrieval:
        print(d)
        print(address)
        _d, key = dot_notation(d, address)
        print(_d)
        print(key)
        _d[key] = kwargs[form]
    d['timeline']['init']['at'] = datetime.now()

    j = json(await orders.insert(options, payload, d, ))
    orders_cache.sync(str(d['crate']['id']), d)
    return j


@bp.route('/<_id>', methods=['DELETE'])
@privileges('dev')
async def _put(request, payload, _id):
    j = json(orders.delete(payload, {'crate.id': _id}))
    orders_cache.delete(_id)
    return j


@bp.route('/<_id>', methods=['GET'])
@privileges('dev')
async def _put(request, payload, _id):
    document = await orders_cache.retrive(_id)
    document['_id'] = str(document['_id'])
    j = json(document)
    return j


@bp.route('/', methods=['GET'])
async def get_all(requests):
    j = await orders.find([], {}, {})
    for doc in j:
        doc['_id'] = str(doc['_id'])
    return json(j)


@bp.route('/<{_id}>/@delay:<{delay}:int>'.format(_id='_id', delay='delay', ), methods=['POST', ])
@privileges('dev', 'applicator', )
async def _delay(request, payload, _id, delay, ):
    options = []

    query = {
        "crate.id": _id
    }

    node = 'timeline.'

    document = await orders_cache.retrieve(_id)

    document['timeline']['ready'] = {
        "by": payload["username"],
        "at": document['timeline']['init']['at'] + timedelta(seconds=delay)
    }

    j = json(await orders.collection.save(document))
    orders_cache.sync('{}.timeline.ready', document['timeline']['ready'])
    return j


@bp.route('/<{_id}>/@status:<{status}>'.format(_id='_id', status='status', ), methods=['POST', ])
@privileges('dev', 'porter', )
async def set_status(request, payload, _id, status, ):
    options = []

    status = statuses.get(status, status)

    query = {
        "crate.id": _id
    }

    d = {
        "by": payload["username"],
        "at": datetime.now()
    }

    j = json(await orders.update(options, payload, query, {
        '$set': {
            'timeline.' + status: d
        }
    }))

    orders_cache.sync('{}.timeline.' + status, d)

    return j


@bp.route('/<_id>/@status:<{status}>'.format(status='status', ), methods=['GET', ])
@privileges('dev', 'porter', 'applicator')
async def get_status(request, payload, _id, status):
    status = statuses.get(status, status)
    try:
        return json(await orders_cache.retrieve(_id)['timeline'][status])
    except:
        return json({'status': 'not found'}, 404)


async def user_trips(request, payload, status, ):
    options = [
        "--me"
    ]

    today = datetime.now()
    today = today.replace(hour=0, minute=0, second=0)
    query = {
        "status": status,
        "_date": {"$gte": today}
    }

    projection = {}
    return json(await orders.find(options, payload, query, projection, ))


@bp.route('/<{_id}>/@road_id=<{road_id}>'.format(_id='_id', road_id='road_id', ), methods=['POST', ])
@privileges('khorus', 'dev', 'operator', )
async def set_road(request, payload, _id, road_id, ):
    options = []

    query = {
        "_id": ObjectId(_id)
    }

    node = "road_id"

    d = ObjectId(road_id)

    operator = "set"

    return json(await orders.update(options, payload, query, node, d, operator, ))


@bp.route('/<order>/@location', methods=['GET'])
@privileges('dev', 'applicator')
async def get_location(request, payload, order, ):
    try:
        user = orders_cache[order]['user']
        return json(users_cache.get(user)['location'])
    except:
        params = [
            {
                "$match": {
                    "order": order
                }
            }, {
                "$lookup": {
                    "from": "locations",
                    "let": {
                        "porter": "$porter"
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$porter", "$$porter"]}
                                    ]
                                }
                            },
                        }, {
                            "$sort": {
                                "_date": -1
                            }
                        }, {
                            "$limit": 1
                        }
                    ],
                    "as": "location"
                }
            }
        ]
        _orders = await orders.collection.aggregate(params).to_list(None)
        return json(_orders)


