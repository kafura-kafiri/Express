from Khorus.Choori.mongo import Bingo
from Khorus.Choori.decorators import privileges, retrieve
from Khorus.config import history as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from Khorus.crud import prime

histories = config['collection']['obj'] = Bingo()
bp = Blueprint(config['name'], url_prefix=config['path'])
