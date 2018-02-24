from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy
import math

# fix random seed for reproducibility
numpy.random.seed(7)

number_of_types = 10
seq = 1
output = 1

model = Sequential()
model.add(LSTM(100, input_shape=(seq, output * 2 * seq + number_of_types)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')


class Scaler:
    def __init__(self, m):
        self.m = m

    def __call__(self, x):
        return 1 / (1 + math.exp(x / self.m))

    def undo(self, x):
        return math.log(1 / x - 1) * self.m


time_s = Scaler(1)
speed_s = Scaler(40)
