import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
from itertools import product, combinations

R = 8.314
vF = 1000

moles = lambda p, v, t: (p*v)/(t*R)

tH = 2300.0
nH = 100000
tC = 230.0
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
plt.subplots_adjust(bottom=0.25)

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
    nF = moles(pF, vF, tF)
    nT = moles(pT, vF, tT)

    tI_given_nR = lambda nR: (tT*nT-tF*(nF-nR))/(nT-nF+nR)
    nR_given_tI = lambda tI: nF+nT*(tI-tT)/(tF-tI)

    # Embedded surface line
    nR = np.linspace(0, nF, 500)
    nI = nT-nF+nR
    tI = (tT*nT-tF*(nF-nR))/nI
    nR[np.where(
        np.logical_or(
            np.logical_or(nR < 0, nR > nF),
            np.logical_or(
                np.logical_or(tI < tC, tI > tH),
                nI < 0
            )
        )
    )] = np.nan
    ax.plot3D(nR, tI, nI, c='red')

    n = 50
    nR = np.linspace(0, nF, n) # nR in [0, nF]
    tI = np.linspace(tC, tH, n) # tI in [tC, tH]
    nR, tI = np.meshgrid(nR, tI)
    nI = (tT*nT-tF*(nF-nR))/tI
    nR[np.where(
        np.logical_or(
            np.logical_or(nR < 0, nR > nF),
            np.logical_or(
                np.logical_or(tI < tC, tI > tH),
                nI < 0
            )
        )
    )] = np.nan
    ax.plot_surface(nR, tI, nI, alpha=0.5)

    tI_ = tI_given_nR(0)
    if tC <= tI_ and tI_ <= tH:
        ax.scatter([0], [nT-nF], [tI_], color='C2')
        print(0, nT-nF, tI_)

    nR_ = nR_given_tI(tC)
    if 0 <= nR_ and nR_ <= nF:
        ax.scatter(
                # np.clip([nR_], 0, nF),
                [nR_],
                [nT-nF+nR_],
                # np.clip([tC], tC, tH),
                [tC],
                color='C0')

    nR_ = nR_given_tI(tH)
    if 0 <= nR_ and nR_ <= nF:
        ax.scatter(
                # np.clip([nR_], 0, nF),
                [nR_],
                [nT-nF+nR_],
                # np.clip([tH], tC, tH),
                [tH],
                color='C3')

    ax.set_xlabel('$n_R$')
    ax.set_ylabel('$t_I$')
    ax.set_zlabel('$n_I$')

    ax.set_xlim3d(0, nF)
    ax.set_zlim3d(0, np.max(nI))

for s in [tTslider, pTslider, tFslider, pFslider]:
    s.on_changed(update)

update()
plt.show()
