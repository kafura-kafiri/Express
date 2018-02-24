from mu import src, dst

base = 10
factor = .5
time_cost = 1
distance_cost = 1
anomaly = 6000


def cost(route):
    steps = route['routes'][0]['legs'][0]['steps']
    print(route['routes'][0]['weight'])
    print(route['routes'][0]['legs'][0]['weight'])
    s = route[]
    d = route[]
    s = src.query(s)
    d = dst.query(d)
    route['routes'][0]['cost'] = \
        factor * time_cost * route['routes'][0]['weight'] + \
        (1 - factor) * distance_cost * route['route'][0]['distance'] + \
        abs(s, d) * anomaly
    s = 0
    if 'ex_distance' in route['routes'][0]:
        route['routes'][0]['ex_cost'] = \
            factor * time_cost * route['routes'][0]['ex_weight'] + \
            (1 - factor) * distance_cost * route['route'][0]['ex_distance']
        s = route['routes'][0]['ex_cost']
        # route['routes'][0]['cost'] += route['routes'][0]['ex_cost']
    return route['routes'][0]['cost'] + s
