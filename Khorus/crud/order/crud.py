from Khorus.Choori.decorators import privileges, retrieve
from Khorus.crud.order import bp, orders
from sanic.response import json
from bson import ObjectId
from datetime import datetime


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
