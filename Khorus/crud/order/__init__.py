import asyncio
import time

import numpy as np
from sanic import Blueprint

from Khorus.Choori.mongo import Bingo
from Khorus.config import order as config
from Map.loop import mus
from Map.mu import Mu
from temp import orders as cached_orders

orders = config['collection']['obj'] = Bingo()
cached_orders.fetch = lambda x: orders.find([], {}, {
    'crate.id': x
})
bp = Blueprint(config['name'], url_prefix=config['path'])


@bp.listener('before_server_start')
async def init(sanic, loop):
    await orders.delete([], {}, {})

import Khorus.crud.order.crud
import Khorus.crud.order.ancillary