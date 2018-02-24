from Khorus.crud.trip import bp, trips
from Khorus.crud.order import orders
from Khorus.Choori.decorators import privileges
from bson import ObjectId
from sanic.response import json


@bp.route('/<{_id}>/<{ack}>'.format(_id='_id', ack='ack', ), methods=['POST', ])
@privileges('dev', 'porter', )
async def ack(request, payload, _id, ack, ):
    options = []

    query = {
        "_id": ObjectId(_id)
    }

    node = "username"

    d = payload['username']  # --username

    operator = "set"

    order_result = await orders.update(options, payload, {"road_id": ObjectId(_id)}, node, d, operator)
    road_result = await trips.update(options, payload, query, node, d, operator, )
    return json([order_result, road_result])
