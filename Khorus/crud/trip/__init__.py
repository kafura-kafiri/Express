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


schema = {

}

default = {

}


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

import Khorus.crud.trip.ancillary
import Khorus.crud.trip.crud