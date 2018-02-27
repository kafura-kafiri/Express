import time
print(time.time())
a = {}
for i in range(4000000):
    a[i] = i / 10
print(time.time())
b = a.values()
print(time.time())
for i in range(4000000):
    a[i] = i / 10
print(time.time())