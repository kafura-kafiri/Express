from Khorus.Choori.mongo import Bingo
from Khorus.Choori.decorators import privileges, retrieve
from Khorus.config import location as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from Khorus.crud import prime

locations = config['collection']['obj'] = Bingo()
bp = Blueprint(config['name'], url_prefix=config['path'])


@bp.route('/send-location', methods=['POST', ])
@privileges('porter', 'dev', )
@retrieve(
    '<lat:num:$form:a>',
    '<lng:num:$form:a>',
)
async def send_location(request, payload, lat, lng, ):
    
    options = [
        "--username",
        "--bulk",
        "--date",
    ]
    
    d = {
        "lat": lat,
        "lng": lng
    }
    
    return json(await locations.insert(options, payload, d, ))