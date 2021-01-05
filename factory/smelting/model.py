import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

R = 8.314
vF = 1000

P = lambda p, v, t: (p*v)/(t*R)

tH = 2200
nH = 100
tC = 200
nC = 100

pMin = 100
pMax = 50000
tMin = 200
tMax = 2300

tT0 = 1500
pT0 = 10000
tF0 = 800
pF0 = 5000

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.25)
plt.suptitle('''\
$t_T n_T=t_F(n_F-n_R)+t_I n_I$
''')
ax.view_init(elev=15, azim=135)
# ax.plot_surface(x, y, z, cmap=plt.cm.coolwarm)

pFax = plt.axes([0.1, 0.05+0.03*3, 0.8, 0.02])
tFax = plt.axes([0.1, 0.05+0.03*2, 0.8, 0.02])
pTax = plt.axes([0.1, 0.05+0.03*1, 0.8, 0.02])
tTax = plt.axes([0.1, 0.05+0.03*0, 0.8, 0.02])

pFslider = Slider(pFax, '$p_F$', pMin, pMax, valinit=pF0)
tFslider = Slider(tFax, '$t_F$', tMin, tMax, valinit=tF0)
pTslider = Slider(pTax, '$p_T$', pMin, pMax, valinit=pT0)
tTslider = Slider(tTax, '$t_T$', tMin, tMax, valinit=tT0)

n = 50 # mesh points per axis

def update(_=None):
    tT, pT, tF, pF = tTslider.val, pTslider.val, tFslider.val, pFslider.val
    nT = P(pT, vF, tT)
    nF = P(pF, vF, tF)
    a = np.linspace(0, nF, n) # nR in [0, nF]
    b = np.linspace(10, nH+nC, n) # nI in [0, nH+nC]
    # x: nR moles removed
    # y: nI moles input
    # z: tI temp input
    x, y = np.meshgrid(a, b)
    fz = np.vectorize(lambda nR, nI: (tT*nT-tF*(nF-nR))/nI)
    z = fz(x, y)
    z = np.ma.masked_outside(fz(x, y), tMin, tMax)
    ax.clear()
    ax.scatter(x, y, z, cmap=plt.cm.coolwarm, vmin=tMin, vmax=tMax)
    ax.set_xlabel('$n_R$ moles removed')
    ax.set_ylabel('$n_I$ moles input')
    ax.set_zlabel('$t_I$ temperature input')
    ax.set_zlim3d(tMin, tMax)

for s in [tTslider, pTslider, tFslider, pFslider]:
    s.on_changed(update)

update()

plt.show()
