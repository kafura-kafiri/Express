from temp import N, E
from temp import n_size, e_size
from multiprocessing import Process
import time
import logging

logger = logging.getLogger('random')
handler = logging.handlers.RotatingFileHandler('random.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def loop():
    while True:
        adj = {}

        for i in range(e_size.value):
            e = E[i]
            if e.v not in adj:
                adj[e.v] = []
            adj[e.v].append((e.u, e.weight))
            # logger.info([e.u, e.v, e.weight])
        for i in range(n_size.value):
            n = N[i]
            es = adj[i]
            if n.type == 0:
                for u, w in es:
                    u = N[u]
                    if u.type == 1:
                        choose(n, u)
        logger.handlers[0].flush()
        time.sleep(5)


def choose(v, u):
    logger.info([v, u])


p = Process(target=loop)
