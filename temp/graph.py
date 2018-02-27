from temp import N, G, max_nodes
from utils.pqdict import pqdict
import time
from Map.backend import osrm_route


async def update_weights(v, U):
    U = [u['location'] for u in U]
    backwards = osrm_route(U, v, reverse=True)
    forwards = osrm_route(U, v, reverse=False)

def add(v, D):

    return i

def update(json):
    now = time.time()
    porters = json.get('users', {})
    orders = json.get('orders', {})
    D = pqdict(key=lambda x: x['_lru'])
    for i in range(max_nodes):
        if N[i]._lru > 0:
            D[N[i]._id] = {
                'location': [N[i].lat, N[i].lng],
                '_lru': now,
                '_i': i,
            }
    for _id, o in orders.items:
        src = o['src']
        dst = o['dst']
        n0 = {
            'location': src,
            '_lru': now
        }
        n1 = {
            'location': dst,
            '_lru': now
        }
        i0 = add(n0, D)
        n0['_i'] = i0
        update_weights(n0, D)
        i1 = add(n1, D)
        n1['_i'] = i1
        update_weights(n1, D)
    for _id, p in porters.items:
        D['3_' + _id] = {
            'location': p['location'],
            '_lru': now
        }
        n = {
            'location': src,
            '_lru': now
        }
        i = add(n, D)
        n0['_i'] = i0
        update_weights(n0, D)