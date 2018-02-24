from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
import random
import numpy as np
import math
from datetime import datetime
import time


class Mu:
    def __init__(self, n_distance, distance_scale=1, time_scale=3600 * 24):
        self.X = []
        self.W = {}
        self.tree = None
        self.n_distance = n_distance
        self.distance_scale = distance_scale
        self.time_scale = time_scale

    def distance(self, v, u):
        return (abs(v[0] - u[0]) ** self.n_distance + abs(v[1] - u[1]) ** self.n_distance + abs(v[2] - u[2]) ** self.n_distance) ** float(1 / self.n_distance)

    def extend(self, X):
        for x in X:
            x[0] /= self.distance_scale
            x[1] /= self.distance_scale
            x[2] = int(x[2])
            x[2] %= 3600 * 24
            x[2] /= self.time_scale

            (w, idx) = self.W.get(tuple(x), (0, len(self.W)))
            w += 1
            if idx == len(self.W):
                self.X.append(x)
            self.W[tuple(x)] = (w, idx)
            self.X[idx] = x
        self.tree = cKDTree(self.X)

    def query(self, x):
        x[2] = int(x[2])
        x[2] %= 3600 * 24
        x[2] /= self.time_scale
        dist, idx = self.tree.query(x, k=12)
        s = 0
        for i in idx:
            s += self.W[tuple(self.X[i])][0]
        s /= self.distance(x, self.X[idx[-1]]) ** 3 * math.pi * 4 / 3
        return s

    def nearest(self, x):
        dist, idx = self.tree.query(x, k=12)
        return [tuple(self.X[i]) for i in idx]

def main():
    mu = Mu(2)
    n = 20
    X = np.random.random((n, 3))
    for x in X:
        x[2] *= 5 * 24 * 3600
    mu.extend(X)
    s = 0
    n = 20
    for i in range(n):
        x = np.random.random((3))
        x[2] *= mu.time_scale
        plt.scatter(x[0], x[1], c='red')
        y = mu.query(x)
        s += y
    print(s / n)
    plt.show()

