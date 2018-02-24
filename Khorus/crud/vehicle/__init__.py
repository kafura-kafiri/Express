from Khorus.Choori.mongo import Bingo
from Khorus.Choori.decorators import privileges, retrieve
from Khorus.config import vehicle as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from Khorus.crud import prime

vehicles = config['collection']['obj'] = Bingo()
bp = Blueprint(config['name'], url_prefix=config['path'])


@bp.route('/init', methods=['POST',])
@privileges('dev', 'admin', 'operator', )
@retrieve(
    '<vehicle_number:str:$form:a>',
    '<vehicle_make:str:$form:a>',
    '<vehicle_model:str:$form:a>',
    '<body_type:str:$form:a>',
    '<capacity:int:$form:a>',
    '<ownership:int:$form:a>',
    '<owner:str:$form:a>',
)
async def create(request, payload, vehicle_number, vehicle_make, vehicle_model, body_type, capacity, ownership, owner, **kwargs):
    
    options = {} 
    
    d = {
        "body": {
            "number": vehicle_number,
            "make": vehicle_make,
            "model": vehicle_model,
            "type": body_type
        },
        "capacity": capacity,
        "ownership": {
            "owner": owner,
            "type": ownership
        }
    } 
    
    return json(await vehicles.insert(options, payload, d, **kwargs))


@bp.route('/<_id>', methods=['POST', ])
@privileges('dev', 'operator', 'admin', )
@retrieve(
    '<_id:id:$uri:a>',
)
async def single_get(request, payload, _id, **kwargs):
    
    options = {} 
    
    q = {
        "_id": _id
    } 
    
    return json(await vehicles.find(options, payload, q, **kwargs))


@bp.route('/all', methods=['POST', ])
@privileges('dev', )
@retrieve(
)
async def all_get(request, payload, **kwargs):
    
    options = {} 
    
    q = {} 
    
    return json(await vehicles.find(options, payload, q, **kwargs))


@bp.route('/:<_id>/@<attr>:<value>', methods=['POST', ])
@privileges('dev', 'admin', 'operator', )
@retrieve(
    '<_id:id:$uri:a>',  # TODO alter
)
async def single_update(request, payload, _id, attr, value, **kwargs):
    
    options = {} 
    
    q = {
        "_id": _id
    } 
    
    updating_json = {
        "$set": {
            attr: value
        }
    }
    
    return json(await vehicles.update(options, payload, q, updating_json, **kwargs))


@bp.route('/:<_id>', methods=['POST', ])
@privileges('dev', )
@retrieve(
    '<_id:id:$uri:a>',
)
async def single_delete(request, payload, _id, **kwargs):
    
    options = {} 
    
    query = {
        "_id": _id
    } 
    
    return json(await vehicles.delete(options, payload, query, **kwargs))
