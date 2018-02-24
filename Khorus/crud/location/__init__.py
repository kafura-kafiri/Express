from Khorus.Choori.mongo import Bingo
from Khorus.config import location as config, crud_path
from sanic import Blueprint
from Khorus.crud import crud

locations = config['collection']['obj'] = Bingo()
bp = Blueprint(config['name'], url_prefix=config['path'])

schema = {
    "porter": '#username',
    "c": ["#lat", "#lng"],
    "#": []
}

default = {
    "porter": "",
    "c": [0, 0],
    "#": []
}

crud(bp, locations, schema, default)
import Khorus.crud.location.ancillary
