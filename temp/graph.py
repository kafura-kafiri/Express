from temp import N, E, n_size, e_size, Node, Edge, String
import ctypes
import time
from Map.backend import osrm_route
from scipy.spatial import cKDTree
import numpy as np
import asyncio
import logging
logger = logging.getLogger('graph')
handler = logging.handlers.RotatingFileHandler(
              'logging.log', backupCount=5)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


async def weights(idx, i):
    U = [[N[j].lat, N[j].lng] for j in idx]
    v = [N[i].lat, N[i].lng]
    forwards = await osrm_route(U, v, reverse=False)
    backwards = await osrm_route(U, v, reverse=True)
    for j, r in enumerate(forwards):
        r = r['routes'][0]
        e = Edge()
        e.weight = r['duration']
        e.v = i
        e.u = j
        logger.debug({'edge': [e.v, e.u, e.weight]})
        E[e_size.value] = e
        e_size.value += 1
    for j, r in enumerate(backwards):
        r = r['routes'][0]
        e = Edge()
        e.weight = r['duration']
        e.v = j
        e.u = i
        logger.debug({'edge': [e.v, e.u, e.weight]})
        E[e_size.value] = e
        e_size.value += 1


def update(json):
    # logger.debug(json)
    now = time.time()
    porters = json.get('users', {})
    orders = json.get('orders', {})
    prev_size = n_size.value
    # append to N -> X
    for _id, (o, node) in orders.items():
        _id = _id[0]
        src = o['transmitter']['coordinates']
        dst = o['receiver']['coordinates']
        n1 = Node()
        n1.lat = src[0]
        n1.lng = src[1]
        n1.lru = now
        n1.type = 1
        s1 = String()
        s1.data = (ctypes.c_char * len(list(_id)))(*[ch.encode() for ch in list(_id)])
        # s1.data = list(_id)
        s1.length = len(list(_id))
        n1.id = s1
        logger.debug(['1', n1.lat, n1.lng, n1.type, n1.id, n1.lru, n1.next])

        n2 = Node()
        n2.lat = dst[0]
        n2.lng = dst[1]
        n2.lru = now
        n2.type = 2
        s2 = String()
        s2.data = (ctypes.c_char * len(list(_id)))(*[ch.encode() for ch in list(_id)])
        # s2.data = list(_id)
        s2.length = len(list(_id))
        n2.id = s2
        logger.debug(['2', n2.lat, n2.lng, n2.type, n2.id, n2.lru, n2.next])

        N[n_size.value] = n1
        n_size.value += 1
        N[n_size.value] = n2
        n_size.value += 1

    for _id, (p, node) in porters.items():
        action = _id[1]
        _id = _id[0]
        if 'location' in p and (action == '+' or node != 'location'):
            n0 = Node()
            n0.lat = float(p['location'][0])
            n0.lng = float(p['location'][1])
            n0.lru = now
            n0.type = 0
            s0 = String()
            s0.data = (ctypes.c_char * len(list(_id)))(*[ch.encode() for ch in list(_id)])
            # s0 = list(_id)
            s0.length = len(list(_id))
            N[n_size.value] = n0
            logger.debug(['0', n0.lat, n0.lng, n0.type, n0.id, n0.lru, n0.next])
            n_size.value += 1
    D = [[n.lat, n.lng] for i, n in enumerate(N) if i < n_size.value]
    if D:
        neighbors = cKDTree(np.array(D))

        async def add_all():
            for i in range(prev_size, n_size.value):
                dist, idx = neighbors.query(np.array([N[i].lat, N[i].lng]), min(20, n_size.value))
                print(idx)
                await weights(idx, i)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(add_all())

    # for _id, o in orders.items():
    #     src = o['src']
    #     dst = o['dst']
    #     n0 = {
    #         'location': src,
    #         '_lru': now
    #     }
    #     n1 = {
    #         'location': dst,
    #         '_lru': now
    #     }
    #     i0 = add(n0, D)
    #     n0['_i'] = i0
    #     update_weights(n0, D)
    #     i1 = add(n1, D)
    #     n1['_i'] = i1
    #     update_weights(n1, D)
    # for _id, p in porters.items():
    #     D['3_' + _id] = {
    #         'location': p['location'],
    #         '_lru': now
    #     }
    #     n = {
    #         'location': src,
    #         '_lru': now
    #     }
    #     i = add(n, D)
    #     n0['_i'] = i0
    #     update_weights(n0, D)
