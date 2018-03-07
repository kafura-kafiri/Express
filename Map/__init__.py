from sanic import Blueprint
from sanic.response import json as jresponse, text
from Map.backend import osrm_route
import ujson as json
import numpy as np
from Map.loop import mus
import numpy as np
import matplotlib.pyplot as plt

bp = Blueprint('map', url_prefix='/map')


# -f, -r, -a.
@bp.route('/<src>:<dst>')
@bp.route('/<src>:<dst>--<options>')
async def route(request, src, dst, options):
    o = {}
    if 'r' in options:
        o['reverse'] = True
    if 'a' in options:
        o['amortized'] = True
    src = src.split(';')
    src = [p.split(',') for p in src]
    src = [[float(x) for x in p] for p in src]
    dst = dst.split(',')
    dst = [float(x) for x in dst]
    return jresponse(await osrm_route(src, dst, **o))


@bp.route('/traffics', methods=['POST'])
async def fit(request):
    traffics = request.form['traffics']
    X = np.array(json.load(traffics))
    X = X.astype('float32')
    fit(X)
    return jresponse({'status': 'OK'})


@bp.route('/mu/<side>/<coordinates>', methods=['GET'])
async def extend(request, side, coordinates):
    side = {
        't': 0,
        'r': 1,
        'transmitter': 0,
        'receiver': 1,
        '0': 0,
        '1': 1
    }[side]
    mu = mus[side]
    coordinates = coordinates.split(';')
    coordinates = [p.split(',') for p in coordinates]
    coordinates = [[float(x) for x in p] for p in coordinates]
    return json([mu.query(c) for c in coordinates])
    points = request.form['points']
    X = np.array(json.load(points))
    X = X.astype('float32')
    # TODO


@bp.route('/contour/<lat>,<lng>', methods=['GET'])
async def contour(request, lat, lng):
    lat = float(lat)
    lng = float(lng)
    dst = [lat, lng]
    n = 21
    scale = float((n - 1) / 2 * 100)
    x, y = np.meshgrid(np.arange(n), np.arange(n))
    x = x.astype('float32')
    y = y.astype('float32')
    half = (n - 1) / 2 * np.ones([n, n])
    x -= half
    y -= half
    x /= scale
    y /= scale
    x += lng * np.ones([n, n])
    y += lat * np.ones([n, n])
    x = x.reshape(n * n)
    y = y.reshape(n * n)
    src = np.array([y, x])
    src = src.transpose()
    routes = await osrm_route(src, dst, reverse=False)
    # for s in src:
    #     print(s, dst)
    #     routes = await osrm_route([s], dst, reverse=False)
    #     r = routes[0]
    #     print(r)
    routes = [r['routes'][0]['distance'] for r in routes]
    cs = plt.contourf(x.reshape(n, n), y.reshape(n, n), np.array(routes).reshape(n, n), corner_mask=False)
    # cs = plt.contourf(x, y, routes, [4, 4.001], corner_mask=False)
    # print(cs.allsegs)
    plt.show()
    return jresponse(4)
