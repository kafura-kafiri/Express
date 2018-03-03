from sanic import Blueprint
from sanic.response import json as jresponse, text
from Map.backend import osrm_route
import ujson as json
import numpy as np
from Map.loop import mus

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