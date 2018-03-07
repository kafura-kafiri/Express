import time
from multiprocessing import Process, Value
from pymongo import MongoClient
from Khorus.config import db_name, order


import numpy as np

from Map.mu import Mu
from Map.osrm import run_osrm

osrm_port = Value('i', 5100)
flag = Value('i', 0)
mus = []


def loop():
    p = []
    while True:
        p.append(run_osrm(osrm_port.value + 1 - flag.value))
        flag.value = 1 - flag.value
        if len(p) > 1:
            p[0].terminate()
            p = p[1:]

        orders = MongoClient()[db_name][order['collection']['name']]
        _orders = orders.find({})  # bad smell <-
        r = [
            [
                *o['receiver']['coordinates'],
                time.mktime(o['timeline']['init']['at'].timetuple())
            ] for o in _orders]
        rm = Mu(2)
        if False:
            rm.extend(np.array(r))
        t = [
            [
                *o['transmitter']['coordinates'],
                time.mktime(o['timeline']['init']['at'].timetuple())
            ] for o in _orders]
        tm = Mu(2)
        if False:
            tm.extend(np.array(t))
        mus.extend([tm, rm])
        while len(mus) > 2:
            mus.pop(0)
            mus.pop(0)
        time.sleep(60 * 60)

# def loop():
#     global mus
#     global flag
#     p = [None, None]
#     while True:
#         mirror = 1 - flag.value
#         p[mirror] = run_osrm(osrm_port.value + mirror)
#         mus[mirror] = Mu(2)
#         orders = MongoClient()[db_name][order['collection']['name']]
#         _orders = orders.find({})
#         _orders = [[o['map']['src'][0], o['map']['src'][1], time.mktime(o['_date'].timetuple())] for o in _orders if '_date' in o and 'map' in o]
#         mus[mirror].extend(np.array(_orders))
#         flag.value = mirror
#         if p[1 - mirror]:
#             p[1 - mirror].terminate()
#         time.sleep(60 * 60)


osrm = Process(target=loop)

if __name__ == '__main__':
    osrm.start()
    osrm.join()
