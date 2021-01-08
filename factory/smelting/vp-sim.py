import numpy as np
import matplotlib.pyplot as plt

v = 1500
n0 = 1000

p = 100

x = np.arange(p)
n = np.full([p], n0)
y = np.ones([p])

r = 20 # L/step
for i in range(1, p//2):
    n[i] = n[i-1]*(1-r/v)
    y[i] = n[i] / n0
r = 60
for i in range(p//2, p):
    n[i] = n[i-1]*(1-r/v)
    y[i] = n[i] / n0

plt.plot(x, y)
plt.ylim(0, 1)
plt.ylabel("Ratio of initial moles")
plt.xlabel("Time")
plt.show()

