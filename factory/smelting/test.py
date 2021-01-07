import numpy as np

a = np.arange(3)
b = np.arange(3)
x, y = np.meshgrid(a, b)

f = np.vectorize(lambda x, y: (x+y))

z = f(x, y)

print(np.array([x, y, z]))

