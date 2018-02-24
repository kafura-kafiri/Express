from Khorus.Choori.mongo import Bingo
from Khorus.Choori.decorators import privileges, retrieve
from Khorus.config import order as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from Khorus.crud import prime, crud
from bson import ObjectId
import datetime

orders = config['collection']['obj'] = Bingo()
bp = Blueprint(config['name'], url_prefix=config['path'])

urls = [
    ('/', 'POST'),
    ('/<_id>', 'GET'),
    ('/<_id>', 'PUT'),
]

schema = {
    'item': {
        'id': '$str',
        "detail": "",
        "#": [],
        'volume': '$int',
    },
    'applicator': {
        'id': '#username',
        'phone': '$str',
    },
    'map': {
        'src': ['$num', '$num', "*str"],
        'dst': ['$num', '$num', "*str"]
    },
    'type': '$int',
    "status": "$int",
    "delay": "*int",
    #  "trip_id": "",
    #  "porter": ""
}

default = {
    'item': {
        'id': '',
        "detail": '',
        "#": [],
        'volume': 0,
    },
    'applicator': {
        'id': '',
        'phone': '',
    },
    'map': {
        'src': [0, 0],
        'dst': [0, 0]
    },
    'type': 0,
    "status": 0,
    "delay": 0,
    #  "trip_id": "",
    #  "porter": ""
}

crud(bp, orders, schema, default)
import Khorus.crud.order.crud
import Khorus.crud.order.ancillary