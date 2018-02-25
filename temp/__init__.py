from temp.cache import Cache
import multiprocessing as mp
import ctypes
import numpy as np

max_nodes = 10000

users = Cache()
orders = Cache()


class Node(ctypes.Structure):
    _fields_ = [('lat', ctypes.c_double),
                ('lng', ctypes.c_double),
                ('id', ctypes.c_long),
                ('lru', ctypes.c_double),]


N = mp.Array(Node, max_nodes)
G_base = mp.Array(ctypes.c_double, max_nodes * max_nodes)
G = np.ctypeslib.as_array(G_base.get_obj())
G = G.reshape(max_nodes, max_nodes)
