import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

R = 8.314
vF = 1000

P = lambda p, v, t: (p*v)/(t*R)

tH = 2300
nH = 100000
tC = 230
nC = 100000

pMin = 100
pMax = 50000
tMin = 200
tMax = 2300

# tT0 = 1500
# pT0 = 4000
tT0 = 1889.00
pT0 = 17948.00

# tF0 = 800
# pF0 = 3000
tF0 = 2108.00
pF0 = 45300.00

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# plt.subplots_adjust(left=0.25, bottom=0.25)
# plt.suptitle('''\
# $t_T n_T=t_F(n_F-n_R)+t_I n_I$
# ''')
# ax.view_init(elev=15, azim=135)

pFax = plt.axes([0.1, 0.05+0.03*3, 0.8, 0.02])
tFax = plt.axes([0.1, 0.05+0.03*2, 0.8, 0.02])
pTax = plt.axes([0.1, 0.05+0.03*1, 0.8, 0.02])
tTax = plt.axes([0.1, 0.05+0.03*0, 0.8, 0.02])

pFslider = Slider(pFax, '$p_F$', pMin, pMax, valinit=pF0)
tFslider = Slider(tFax, '$t_F$', tMin, tMax, valinit=tF0)
pTslider = Slider(pTax, '$p_T$', pMin, pMax, valinit=pT0)
tTslider = Slider(tTax, '$t_T$', tMin, tMax, valinit=tT0)

n = 1000 # mesh points per axis

def update(_=None):
    global nR
    global nI
    global tI
    tT, pT, tF, pF = tTslider.val, pTslider.val, tFslider.val, pFslider.val
    nT = P(pT, vF, tT)
    nF = P(pF, vF, tF)
    nR = np.linspace(0, nF, n) # nR in [0, nF]
    nI = np.linspace(10, nH+nC, n) # nI in [0, nH+nC]
    # x: nR moles removed
    # y: nI moles input
    # z: tI temp input
    nR, nI = np.meshgrid(nR, nI)
    ftI = np.vectorize(lambda nR, nI: (tT*nT-tF*(nF-nR))/nI)
    # tI = ftI(nR, nI)
    tI = np.ma.masked_outside(ftI(nR, nI), tMin, tMax)
    ax.clear()
    # ax.plot_surface(nR, nI, tI)
    ax.scatter([1809.22], [367.37], [1426.77], color='red')
    ax.scatter(nR, nI, tI, alpha=.1)
    ax.set_xlabel('$n_R$ moles removed')
    ax.set_ylabel('$n_I$ moles input')
    ax.set_zlabel('$t_I$ temperature input')
    ax.set_xlim3d(0, np.max(nR))
    ax.set_zlim3d(tMin, tMax)


for s in [tTslider, pTslider, tFslider, pFslider]:
    s.on_changed(update)

update()

print(np.nanmin(np.array([nR, nI, tI]), axis=(1,2), keepdims=True))

plt.show()
