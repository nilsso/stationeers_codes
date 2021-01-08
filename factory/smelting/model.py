import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
from itertools import product, combinations

R = 8.314
vF = 1000

P = lambda p, v, t: (p*v)/(t*R)

tH = 2300
nH = 100000
tC = 230
nC = 100000

pMin = 100
pMax = 50000

# tT0 = 1500
# pT0 = 4000
tT0 = 2100
pT0 = 40000

# tF0 = 800
# pF0 = 3000
tF0 = 2050
pF0 = 38000

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
tFslider = Slider(tFax, '$t_F$', tC, tH, valinit=tF0)
pTslider = Slider(pTax, '$p_T$', pMin, pMax, valinit=pT0)
tTslider = Slider(tTax, '$t_T$', tC, tH, valinit=tT0)

def update(_=None):
    ax.clear()
    tT, pT, tF, pF = tTslider.val, pTslider.val, tFslider.val, pFslider.val
    nT = P(pT, vF, tT)
    nF = P(pF, vF, tF)

    nR = np.linspace(0, nF, 500)
    nI = nT-nF+nR
    tI = (tT*nT-tF*(nF-nR))/nI
    nR[np.where(
        np.logical_or(
            np.logical_or(tI < tC, tI > tH),
            nI < 0
        )
    )] = np.nan
    # tI = np.clip(tI, tC, tH)
    ax.plot3D(nR, tI, nI, c='red')

    n = 50
    nR = np.linspace(0, nF, n) # nR in [0, nF]
    tI = np.linspace(tC, tH, n) # tI in [tC, tH]
    nR, tI = np.meshgrid(nR, tI)
    nI = (tT*nT-tF*(nF-nR))/tI
    nR[np.where(
        np.logical_or(
            np.logical_or(tI < tC, tI > tH),
            nI < 0
        )
    )] = np.nan
    ax.plot_surface(nR, tI, nI, alpha=0.5)

    ax.set_xlabel('$n_R$')
    ax.set_ylabel('$t_I$')
    ax.set_zlabel('$n_I$')

    ax.set_xlim3d(0, nF)
    ax.set_zlim3d(0, np.max(nI))

for s in [tTslider, pTslider, tFslider, pFslider]:
    s.on_changed(update)

update()

# print(np.nanmin(np.array([nR, nI, tI]), axis=(1,2), keepdims=True))

plt.show()
