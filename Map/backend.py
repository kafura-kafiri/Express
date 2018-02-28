import osrm
import time
import numpy as np
from Map.loop import flag, osrm_port, mus


async def osrm_route(src, dst, reverse=False, amortized=False):
    X, T = 0, 0
    if amortized:
        expected_src = mus[flag.value].nearest(np.array(dst))
        expected_routes = osrm_route(expected_src, dst, reverse=True)
        for r in expected_routes:
            X += r['routes'][0]['distance']
            T += r['routes'][0]['duration']
        X /= len(expected_routes)
        T /= len(expected_routes)
    client = osrm.AioHTTPClient(host='http://localhost:{}'.format(osrm_port.value + flag.value))
    response = []
    for s in src:
        r = await client.route(
            coordinates=[s, dst] if not reverse else [dst, s],
            overview=osrm.overview.full,
            steps=True,
            geometries=osrm.geometries.polyline,
        )
        r['routes'][0]['distance'] += X
        r['routes'][0]['duration'] += T
        response.append(r)
    await client.close()
    return response


def optimize(route, now):
    steps = route['routes'][0]['legs'][0]['steps']
    print(route['routes'][0]['weight'])
    print(route['routes'][0]['legs'][0]['weight'])
    d = 0
    for step in steps:
        if step['weight']:
            _speed = step['distance'] / step['weight']
            # _speed = predict(_speed, now)
            step['weight'] = step['distance'] / _speed
            step['duration'] = step['weight']
            d += step['weight']
    route['routes'][0]['legs'][0]['weight'] = d
    route['routes'][0]['weight'] = d
    route['routes'][0]['duration'] = d
    route['routes'][0]['legs'][0]['duration'] = d
    return route


async def optimized_route(src, dst):
    client = osrm.AioHTTPClient(host='http://localhost:5555')
    response = []
    now = time.time()
    for s in src:
        route = await client.route(
            coordinates=[s, dst],
            overview=osrm.overview.full,
            steps=True,
            geometries=osrm.geometries.polyline,
        )

        response.append(optimize(route, now))
    await client.close()
    return response
