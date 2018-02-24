import numpy as np


def distance(v, u, n=2):
    return (abs(v[0] - u[0]) ** n + abs(v[1] - u[1]) ** n) ** float(1 / n)


def speed(prev, x, next):
    prev_d = distance(prev, x)
    next_d = distance(next, x)
    t1 = abs(x[2] - prev[2])
    t2 = abs(x[2] - next[2]) + t1
    x1 = prev_d
    x2 = x1 + next_d
    a = np.array([[t1 ** 2, t1], [t2 ** 2, t2]])
    b = np.array([x1, x2])
    x = np.linalg.solve(a, b)
    return 2 * x[0] * t1 + x[1]


x1 = [3, 1, 4]
x2 = [1, 3, 5]
x3 = [3, 3, 6]

print(speed(x1, x2, x3))
