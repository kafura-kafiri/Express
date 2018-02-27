from Khorus.Choori.decorators import privileges, retrieve
from Khorus.crud.order import bp, orders, schema, default
from sanic.response import json
from bson import ObjectId
from datetime import datetime
from temp import orders as orders_cache, users as users_cache
from utils import to_list, dot_notation
from copy import deepcopy


retrieval = to_list(schema)
hashtags = [(feature[0], feature[1][1:]) for feature in retrieval if '#' in feature[1]]
retrieval = ['<{key}:{type}:$form:k>'.format(key=feature[0], type=feature[1][1:])
             for feature in retrieval if '$' in feature[1]]


@bp.route('/', methods=['POST'])
@bp.route('/<_id>', methods=['POST'])
@privileges('dev', 'operator', 'applicator')
@retrieve(
    *retrieval
)
async def _put(request, payload, _id=None, **kwargs):
    options = [
        "--date"
    ]

    d = deepcopy(default)
    for key, tag in hashtags:
        _d, key = dot_notation(d, key)
        _d[key] = payload[tag]

    if _id:
        d['_id'] = ObjectId(_id)

    for key, value in kwargs.items():
        _d, key = dot_notation(d, key)
        _d[key] = value
    j = json(await orders.insert(options, payload, d, ))
    orders_cache.sync(str(d['_id']), d)
    return j


@bp.route('/<_id>', methods=['DELETE'])
@privileges('dev')
async def _put(request, payload, _id):
    j = json(orders.delete(payload, {'_id': ObjectId(_id)}))
    orders_cache.delete(_id)
    return j


@bp.route('/<_id>', methods=['GET'])
@privileges('dev')
async def _put(request, payload, _id):
    try:
        document = orders_cache.get(_id)
    except:
        document = orders.find(payload, {'_id': ObjectId(_id)})[0]
    document['_id'] = str(document['_id'])
    j = json(document)
    return j


@bp.route('/<{_id}>/@delay:<{delay}:int>'.format(_id='_id', delay='delay', ), methods=['POST', ])
@privileges('dev', 'applicator', )
async def _delay(request, payload, _id, delay, ):
    options = []

    query = {
        "_id": ObjectId(_id)
    }

    node = "delay"

    d = int(delay)

    operator = "inc"

    return json(await orders.update(options, payload, query, node, d, operator, ))


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


@bp.route('/@status:<{status}>'.format(status='status', ), methods=['POST', ])
@privileges('dev', 'porter', )
@retrieve(
)
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


@bp.route('/<order>/@status:<{status}>'.format(status='status', ), methods=['GET', ])
@privileges('dev', 'porter', 'applicator')
async def get_status(request, payload, order):
    try:
        return json(orders_cache[order]['status'])
    except:
        options = []
        query = {
            "order": order,
        }
        return json(await orders.find(options, payload, query))


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
