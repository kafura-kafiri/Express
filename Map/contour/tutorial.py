import matplotlib.pyplot as plt
import numpy as np

# Data to plot.
for i in range(10):
    x, y = np.meshgrid(np.arange(11), np.arange(11))
    five = 5 * np.ones([11, 11])
    five = five.astype('int')
    x -= five
    y -= five
    z = np.power(np.power(x, 2) + np.power(y, 2), .5)
    # z = np.sin(0.5 * x) * np.cos(0.41 * y)

    cs = plt.contourf(x, y, z, [4, 4.001], corner_mask=False)
    print(cs.allsegs)
# plt.show()