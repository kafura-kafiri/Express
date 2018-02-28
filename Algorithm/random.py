from temp import N, E
from temp import n_size, e_size
from multiprocessing import Process
import time


def loop():
    adj = {}
    for i in range(e_size.value):
        e = E[i]
        if e.v not in adj:
            adj[e.v] = []
        adj[e.v].append(e.u)
        adj[e.v] = (e.u, e.weight)

    print('************************************')
    print('************************************')
    
    for i in range(n_size.value):
        print(i, adj[i])
    time.sleep(5)


p = Process(target=loop)