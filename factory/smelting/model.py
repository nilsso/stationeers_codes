import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

R = 8.314
vF = 1000

P = lambda p, v, t: (p*v)/(t*R)

tH = 2200
nH = 100
tC = 200
nC = 100

# tT = 1200
# pT = 200
# tF = 1500
# pF = 500

tT = 1500
pT = 500
tF = 1000
pF = 100

nT = P(pT, vF, tT)
nF = P(pF, vF, tF)

n = 50

# tT*nT = tF*(nF-x)+yz
# x: tI temp input
# y: nI moles input
# z: nR moles removed
# fz = np.vectorize(lambda x, y: 0)
fz = np.vectorize(lambda x, y: nF-(tT*nT-x*y)/tF)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

a = np.linspace(tC, tH, n) # tI
b = np.linspace(0, nH+nC, n) # nI
x, y = np.meshgrid(a, b)
z = fz(x, y)
ax.plot_surface(x, y, z, cmap=plt.cm.coolwarm)
ax.set_xlabel('$t_I$ temperature input')
ax.set_ylabel('$n_I$ moles input')
ax.set_zlabel('$n_R$ moles removed')

plt.title('$t_T n_T=t_F(n_F-n_R)+t_I n_I$')
plt.show()
