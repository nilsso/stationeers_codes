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
tT0 = 700
pT0 = 8000

# tF0 = 800
# pF0 = 3000
tF0 = 600
pF0 = 6000

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=22, azim=135)
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

    print(nF, nT)

    tI_given_nR = lambda nR: (tT*nT-tF*(nF-nR))/(nT-nF+nR)
    nR_given_tI = lambda tI: nF+nT*(tI-tT)/(tF-tI)

    # Embedded surface line
    nR = np.linspace(0, nF, 500)
    nI = nT-nF+nR
    tI = (tT*nT-tF*(nF-nR))/nI
    mask = np.logical_or(
        np.logical_or(nR < 0, nR > nF),
        np.logical_or(
            np.logical_or(tI < tC, tI > tH),
            nI < 0
        )
    )
    nR[np.where(mask)] = np.nan
    tI[np.where(mask)] = np.nan
    nI[np.where(mask)] = np.nan
    ax.plot3D(nR, tI, nI, c='red')

    # Surface
    n = 50
    nR = np.linspace(0, nF, n) # nR in [0, nF]
    tI = np.linspace(tC, tH, n) # tI in [tC, tH]
    nR, tI = np.meshgrid(nR, tI)
    nI = (tT*nT-tF*(nF-nR))/tI
    mask = np.logical_or(
        np.logical_or(nR < 0, nR > nF),
        np.logical_or(
            np.logical_or(tI < tC, tI > tH),
            nI < 0
        )
    )
    nR[np.where(mask)] = np.nan
    ax.plot_surface(nR, tI, nI, alpha=0.5)
    ax.set_xlim3d(0, nF)
    ax.set_zlim3d(-10, np.max(nI))

    tI[np.where(mask)] = np.nan
    nI[np.where(mask)] = np.nan
    # print(np.nanmin(nI))

    nR_ = 0
    tI_ = (tT*nT-tF*(nF-nR_))/(nT-nF+nR_)
    nI_ = nT-nF
    nH_ = nI_*(tI_-tC)/(tH-tC)
    nC_ = nI_-nH_
    tT_ = (tF*(nF-nR_)+tC*nC_+tH*nH_)/(nF-nR_+nC_+nH_)
    if nR_ >= 0 and nH_ >= 0 and nC_ >= 0:
        ax.scatter([nR_], [tI_], [nI_], color='C2') # green
    print(f'nR:{nR_:.1f} tI:{tI_:.1f} nH:{nH_:.1f} nC:{nC_:.1f} tT:{tT_:.1f}')

    tI_ = tC
    nR_ = nF-(nT*(tT-tC))/(tF-tC)
    nI_ = nT-nF+nR_
    nH_ = nI_*(tI_-tC)/(tH-tC)
    nC_ = nI_-nH_
    tT_ = (tF*(nF-nR_)+tC*nC_+tH*nH_)/(nF-nR_+nC_+nH_)
    if nR_ >= 0 and nH_ >= 0 and nC_ >= 0:
        ax.scatter([nR_], [tI_], [nI_], color='C0') # blue
    # print(f'nR:{nR_:.1f} tI:{tI_:.1f} nH:{nH_:.1f} nC:{nC_:.1f} tT:{tT_:.1f}')

    tI_ = tH
    nR_ = nF-(nT*(tT-tH))/(tF-tH)
    nI_ = nT-nF+nR_
    nH_ = nI_*(tI_-tC)/(tH-tC)
    nC_ = nI_-nH_
    tT_ = (tF*(nF-nR_)+tC*nC_+tH*nH_)/(nF-nR_+nC_+nH_)
    if nR_ >= 0 and nH_ >= 0 and nC_ >= 0:
        ax.scatter([nR_], [tI_], [nI_], color='C3') # red
    # print(f'nR:{nR_:.1f} tI:{tI_:.1f} nH:{nH_:.1f} nC:{nC_:.1f} tT:{tT_:.1f}')

    # x = [0.0, np.nanmax(nF)]
    # y = [tC, tH]
    # x, y = np.meshgrid(x, y)
    # z = np.zeros(x.shape)
    # ax.plot_surface(x, y, z, color='C2')

    # tI_ = tI_given_nR(0)
    # nI_ = nT-nF
    # tI_ = (tT*nT-tF*nF)/nI_
    # nH_ = nI_*(tI_-tC)/(tH-tC)
    # nC_ = nI_-nH_
    # if nH_ >= 0 and nC_ >= 0:
    #     ax.scatter([0], [tI_], [nI_], color='C2') # green
    # print(nH_, nC_);

    #tI_ = tC
    #nR_ = nF-(nT*(tT-tC))/(tF-tC)
    #nI_ = nT-nF+nR_
    ##if 0 <= nR_ and nR_ <= nF:
    #ax.scatter(
    #        # np.clip([nR_], 0, nF),
    #        [nR_],
    #        [tI_],
    #        # np.clip([tC], tC, tH),
    #        [nI_],
    #        color='C0') # blue

    #nR_ = nR_given_tI(tH)
    #if 0 <= nR_ and nR_ <= nF:
    #    ax.scatter(
    #            # np.clip([nR_], 0, nF),
    #            [nR_],
    #            [nT-nF+nR_],
    #            # np.clip([tH], tC, tH),
    #            [tH],
    #            color='C3')

    ax.set_xlabel('$n_R$')
    ax.set_ylabel('$t_I$')
    ax.set_zlabel('$n_I$')

for s in [tTslider, pTslider, tFslider, pFslider]:
    s.on_changed(update)

update()
plt.show()
