from Khorus.Choori.mongo import Bingo
from Khorus.Choori.decorators import privileges, retrieve
from Khorus.config import order as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from Khorus.crud import prime
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
    'item': {},
    'applicator': '',
    'map': {},
}
