from temp import G, N, users, orders
from temp.cache import CacheAlert


# create pqdict
def update_graph(json):
    print(json)
    print('huli huli')


async def update():
    pass

if __name__ == "__main__":
    ca = CacheAlert(update_graph, users=users, orders=orders)
    users.sync('t.e', 5)
