from utils.pqdict import pqdict
import time
from utils import dot_notation
from threading import Thread


class Cache:
    def __init__(self, max_size=100000):
        self.q = {}
        self.pd = pqdict(key=lambda x: x['_lru'])
        self.max_size = max_size

    def sync(self, node, value):
        node = node.split('.')
        key, node = node[0], '.'.join(node[1:])
        if key not in self.pd:
            if len(self.pd) == self.max_size:
                key, value = self.pd.popitem()
                self.q[(key, '-')] = value

        if not node:
            value['_lru'] = time.time()
            self.pd[key] = value

        if node:
            if key not in self.pd:
                self.pd[key] = {
                    '_lru': time.time()
                }
            v, node = dot_notation(self.pd, key + '.' + node)
            v[node] = value
            self.pd[key]['_lru'] = time.time()

        self.q[(key, '+')] = self.pd[key]

    """
    def sync(collection, node, d):
    keys = node.split('.')
    for key in keys[:-1]:
        if key not in collection:
            collection[key] = {}
        collection = collection[key]
    collection[keys[-1]] = d
    if len(keys) == 1:
        collection[keys[-1]]['_lru'] = time.time()
    """

    def get(self, key):
        v = self.pd[key]
        v['_lru'] = time.time()
        return v


class CacheAlert:
    def __init__(self, alert, **kwargs):
        self.temps = kwargs
        self.alert = alert
        self.t = Thread(target=self._loop)
        self.t.start()

    def _loop(self):
        while True:
            sleep = 1
            data = {}
            for name, t in self.temps.items():
                if t.q:
                    data[name] = {}
                    data[name].update(t.q)
                    t.q.clear()
            if data:
                self.alert(data)
                sleep += 9
            time.sleep(sleep)


if __name__ == "__main__":
    def alert(json):
        print(json)
    from temp import users, orders
    ca = CacheAlert(alert, users=users, orders=orders)
    users.sync('t.e', 5)
