from lstm.model import model, time_s, speed_s
import numpy as np

y = 0  # bad smell. if system down it start from the beginning.
_t = 0
def predict(t, w):
    global y, _t
    y = model.predict(np.array([time_s(t - _t), w, y]))
    _t = t
    return speed_s.undo(y)


def fit(X):
    food = []
    prev = X[0]
    for x in X[1:]:
        food.append([x[0] - prev[0], x[1], prev[2], x[2]])
        x[0] = time_s(x[0])
        x[2] = speed_s(x[2])
        prev = x
    model.fit(np.array(food))
