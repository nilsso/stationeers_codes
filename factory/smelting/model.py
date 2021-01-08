import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

R = 8.314
vF = 1000

P = lambda p, v, t: (p*v)/(t*R)

tH = 2300.0
nH = 100000
tC = 230.0
nC = 100000

pMin = 100
pMax = 50000
tMin = 200
tMax = 2300

tT0 = 300
pT0 = 50000
# tT0 = 1889.00
# pT0 = 17948.00

tF0 = 200
pF0 = 40000
# tF0 = 2108.00
# pF0 = 45300.00

# fig, ax = plt.subplots()
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# ax3 = fig.add_subplot(313)
plt.subplots_adjust(bottom=0.25)

pFax = plt.axes([0.1, 0.05+0.03*3, 0.8, 0.02])
tFax = plt.axes([0.1, 0.05+0.03*2, 0.8, 0.02])
pTax = plt.axes([0.1, 0.05+0.03*1, 0.8, 0.02])
tTax = plt.axes([0.1, 0.05+0.03*0, 0.8, 0.02])

pFslider = Slider(pFax, '$p_F$', pMin, pMax, valinit=pF0)
tFslider = Slider(tFax, '$t_F$', tMin, tMax, valinit=tF0)
pTslider = Slider(pTax, '$p_T$', pMin, pMax, valinit=pT0)
tTslider = Slider(tTax, '$t_T$', tMin, tMax, valinit=tT0)

n = 30 # mesh points
zero = np.zeros([n])

def update(_=None):
    # tT, pT, tF, pF = tT0, pT0, tF0, pF0
    tT, pT, tF, pF = tTslider.val, pTslider.val, tFslider.val, pFslider.val
    nF = P(pF, vF, tF)
    nT = P(pT, vF, tT)

    nR = np.linspace(0, nF, n)
    nI = nT-nF+nR
    tI = (tT*nT-tF*(nF-nR))/nI
    # tI = np.clip((tT*nT-tF*(nF-nR))/nI, tC, tH)

    mask = np.full([n], False)
    mask = np.logical_or(mask, tI < tC)
    mask = np.logical_or(mask, tI > tH)
    mask = np.logical_or(mask, nI < 0)

    nR = np.ma.masked_where(mask, nR)
    nI = np.ma.masked_where(mask, nI)
    tI = np.ma.masked_where(mask, tI)

    # tI_ = min(tH, max(tC, (tF*nF-tT*nT)/(nT+nF)))
    tI_ = (tF*nF-tT*nT)/(nT+nF)
    nR_ = nF-(tT*nT+tI_*nT)/(tF-tI_)
    print(f'{tI_:.2f}, {nR_:.2f}')

    ax1.clear()
    ax1.plot(nR, nI)
    # ax1.set_xlim(0, nF)
    # ax1.set_ylim(0, np.ma.log10(np.max(nI)))
    ax1.set_xlabel('Moles removed $n_R$')
    ax1.set_ylabel('Moles added $n_I$')
    # ax1.set_title(f'$n_F={nF:n}$')

    ax2.clear()
    ax2.plot(nR, tI)
    # ax2.set_xlim(0, nF)
    # ax2.set_ylim(np.log10(tC), np.log10(tH))
    ax2.set_xlabel('Moles removed $n_R$')
    ax2.set_ylabel('Temperature of moles added $t_I$')

    # ax3.clear()
    # ax3.plot(nR, (tF*(nF-nR)+tI*nI)/(nF-nR+nI))
    # ax3.set_xlim(0, nF)

for s in [tTslider, pTslider, tFslider, pFslider]:
    s.on_changed(update)

update()
plt.show()
