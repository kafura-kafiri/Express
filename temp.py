from multiprocessing import Manager
from multiprocessing.managers import BaseManager
from utils.pqdict import pqdict
import time

BaseManager.register('pqdict', pqdict)
manager = BaseManager()
manager.start()
users = manager.pqdict(key=lambda model: model['_lru'])
orders = manager.pqdict(key=lambda model: model['_lru'])
G = manager.pqdict(key=lambda model: model['_lru'])


def sync(collection, node, d):
    keys = node.split('.')
    for key in keys[:-1]:
        if key not in collection:
            collection[key] = {}
        collection = collection[key]
    collection[keys[-1]] = d
    if len(keys) == 1:
        collection[keys[-1]]['_lru'] = time.time()

# todo sync all
# todo add sync to all endpoints


