from pandas import DataFrame
import datetime
import random
import numpy as np


def gaussian(x, sig):

    return np.exp(-np.power(x, 2.) / (2 * np.power(sig, 2.)))

def simulate(x):
    x1 = x - 13 * 3600
    x2 = x - 21 * 3600
    x1 = float(x1) / 3600
    g1 = gaussian(x1, 2)
    g2 = gaussian(x2, 2)
    return (g1 + g2) / 2

yesterday = datetime.datetime.now() - datetime.timedelta(days=2)
data = []
for i in range(100):
    x = random.randint(0, 30)
    yesterday += datetime.timedelta(minutes=x)
    t = (yesterday.hour * 60 + yesterday.minute) * 60 + yesterday.second
    data.append([yesterday, 0, simulate(t)])

df = DataFrame(data, columns=["Date", "Type", "Factor"])
df.to_csv('traffics1.csv')