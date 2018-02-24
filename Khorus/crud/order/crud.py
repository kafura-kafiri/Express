from Khorus.Choori.decorators import privileges, retrieve
from Khorus.crud.order import bp, orders
from sanic.response import json


@bp.route('/', methods=['POST', ])
@privileges('dev', 'applicator', )
@retrieve(
    '<dict:form:object>',
    '<list:form:src>',
    '<list:form:dst>',
    '<num:form:delay>',
)
async def init(request, payload, object, src, dst, delay, ):
    options = [
        "--date"
    ]

    d = {
        "applicator": payload['username'],
        "object": object,
        "src": src,
        "dst": dst,
        "status": "init",
        "delay": delay,
    }

    return json(await orders.insert(options, payload, d, ))


@bp.route('/<{_id}>/@delay:<{delay}>'.format(_id='_id', delay='delay', ), methods=['POST', ])
@privileges('dev', 'applicator', )
@retrieve(
)
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
@retrieve(
)
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

    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0)
    query = {
        "status": status,
        "_date": {"$gte": today}
    }

    projection = {}

    return json(await orders.find(options, payload, query, projection, ))
