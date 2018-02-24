import pandas
import datetime
from lstm_configure import number_of_types
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


'''[1 if _type == i else 0 for i in range(number_of_types)]'''

data = pandas.read_csv('traffics1.csv', usecols=[1, 2, 3])
data = data.values
start = datetime.datetime.strptime(data[0, 0], '%Y-%m-%d %H:%M:%S.%f')
for i, date in enumerate(data[:, 0]):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    delta = date - start
    start = date
    data[i, 0] = delta.total_seconds()
y = pandas.DataFrame(data[:, 2])
types = []
for _type in data[:, 1]:
    types.append(
        (lambda x: [1 if x == i else 0 for i in range(number_of_types)])(_type)
    )

time = data[:, 0]
scaler = MinMaxScaler(feature_range=(0, 1))  # -<

data = time.reshape(time.shape[0], 1)
data = scaler.fit_transform(data)
data = np.append(data, types, axis=1)
data = np.append(data, y.shift(+1), axis=1)

from lstm.model import model, seq
data = data.reshape(data.shape[0], seq, data.shape[1])
data = data.astype('float32')
data = data[1:]
y = y[1:]
model.fit(data, y, epochs=10, batch_size=1, verbose=2)
prediction = model.predict(data)
z = model.predict(data[0:1])
print(z)
plt.plot(y)
plt.plot(prediction)
plt.show()