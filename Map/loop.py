from multiprocessing import Process, Value
from Map.mu import Mu
from Map.osrm import run_osrm
from Khorus.config import db_name, order
from pymongo import MongoClient
import numpy as np
import time
osrm_port = Value('i', 5100)
flag = Value('i', 0)
mus = [None, None]


def loop():
    global mus
    global flag
    p = [None, None]
    while True:
        mirror = 1 - flag.value
        p[mirror] = run_osrm(osrm_port.value + mirror)
        mus[mirror] = Mu(2)
        orders = MongoClient()[db_name][order['collection']['name']]
        _orders = orders.find({})
        _orders = [[o['map']['src'][0], o['map']['src'][1], time.mktime(o['_date'].timetuple())] for o in _orders if '_date' in o and 'map' in o]
        mus[mirror].extend(np.array(_orders))
        flag.value = mirror
        if p[1 - mirror]:
            p[1 - mirror].terminate()
        time.sleep(60 * 60)


osrm = Process(target=loop)

if __name__ == '__main__':
    osrm.start()
    osrm.join()
