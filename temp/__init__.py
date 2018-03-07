from temp.cache import Cache, CacheAlert
import multiprocessing as mp
import ctypes
import numpy as np

max_nodes = 1000

users = Cache()
orders = Cache()


class String(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(ctypes.c_char)),
        ('length', ctypes.c_long)
    ]


class Edge(ctypes.Structure):
    _fields_ = [
        ('weight', ctypes.c_float),
        ('v', ctypes.c_long),
        ('u', ctypes.c_long)
    ]


class Node(ctypes.Structure):
    _fields_ = [
        ('lat', ctypes.c_double),
        ('lng', ctypes.c_double),
        ('type', ctypes.c_int),
        ('id', String),
        ('lru', ctypes.c_double),
        ('next', ctypes.c_int)
    ]


E = mp.Array(Edge, max_nodes * max_nodes)
N = mp.Array(Node, max_nodes)

n_size = mp.Value(ctypes.c_int)
e_size = mp.Value(ctypes.c_int)

# G_base = mp.Array(ctypes.c_double, max_nodes * max_nodes * 2)
# G = np.ctypeslib.as_array(G_base.get_obj())
# G = G.reshape(max_nodes, max_nodes, 2)


from temp.graph import update
ca = CacheAlert(update, users=users, orders=orders)
