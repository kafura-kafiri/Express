from Khorus.Choori.mongo import Bingo
from Khorus.config import location as config, crud_path
from sanic import Blueprint

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


@bp.listener('before_server_start')
async def init(sanic, loop):
    await locations.delete([], {}, {})

import Khorus.crud.location.ancillary
