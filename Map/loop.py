from multiprocessing import Process, Value
from multiprocessing.managers import BaseManager
from Map.mu import Mu
from Map.osrm import run_osrm
from Khorus.config import db_name, order
from pymongo import MongoClient
import numpy as np
import time

BaseManager.register('Mu', Mu)
manager = BaseManager()
manager.start()
base_port = 5100
flag = Value('i', 0)
mus = [None, None]


def loop():
    global mus
    global flag
    p = [None, None]
    while True:
        mirror = 1 - flag.value
        p[mirror] = run_osrm(base_port + mirror)
        mus[mirror] = manager.Mu(2)
        orders = MongoClient()[db_name][order['collection']['name']]
        _orders = orders.find({})
        _orders = [[o['src'][0], o['src'][1], time.mktime(o['_date'].timetuple())] for o in _orders]
        mus[mirror].extend(np.array(_orders))
        flag.value = mirror
        if p[1 - mirror]:
            p[1 - mirror].terminate()
        time.sleep(10 * 60)


osrm = Process(target=loop)

if __name__ == '__main__':
    osrm.start()
    osrm.join()
