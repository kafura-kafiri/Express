from Khorus.Choori.mongo import Bingo
from Khorus.Choori.decorators import privileges, retrieve
from Khorus.config import trip as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from Khorus.crud import prime
import datetime
from bson import ObjectId
from Khorus.crud.order import orders

trips = config['collection']['obj'] = Bingo()
bp = Blueprint(config['name'], url_prefix=config['path'])


@bp.route('/init/'.format(), methods=['POST', ])
@privileges('dev', 'khorus', 'operator', )
@retrieve(
    '<num:form:src_lat>',
    '<num:form:src_lng>',
    '<num:form:dst_lat>',
    '<num:form:dst_lng>',
    '<str:form:username>',
)
async def init(request, payload, src_lng, src_lat, dst_lng, dst_lat, username, ):
    
    options = [
        "--date",
    ]
    
    d = {
        "src": [
            src_lat,
            src_lng
        ],
        "dst": [
            dst_lat,
            dst_lng
        ],
        "username": username
    }
    
    return json(await trips.insert(options, payload, d, ))


@bp.route('/<{_id}>/<{ack}>'.format(_id='_id', ack='ack', ), methods=['POST', ])
@privileges('dev', 'porter', )
@retrieve(
)
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
