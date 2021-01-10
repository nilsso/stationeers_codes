from random import random

R = 8.31446261815324
cp = 28.2 # CO2

def moles(p, v, t):
    return (p*v)/(R*t)

vF = 1000
vI = 1500
vH = 500
vC = 500

tH = 2300 # hot source temperature
tC = 230 # cold source temperature

# tT = 1000
# pT = 10000
tT = tC+random()*(tH-tC)
pT = random()*60000
# tT = 980.17
# pT = 6389.91

# tF = 500
# pF = 800
tF = tC+random()*(tH-tC)
pF = random()*60000
# tF = 978.15
# pF = 55593.88

class Params:
    def __init__(self, t, p, v):
        self.t = t
        self.p = p
        self.v = v

    def unpack(self):
        return self.t, moles(self.p, self.v, self.t)

def findSolution(Tparams, Fparams, tH, tC, nRs):
    tT, nT = Tparams.unpack()
    tF, nF = Fparams.unpack()
    nR = 0
    nI = nT-nF+nR
    tI = (tT*nT-tF*(nF-nR))/nI
    nH = nI*(tI-tC)/(tH-tC)
    nC = nI-nH
    while nH < 0 or nC < 0 and nR <= nF:
        nR += nRs
        nI = nT-nF+nR
        tI = (tT*nT-tF*(nF-nR))/nI
        nH = (tI*nI-tC*nI)/(tH-tC)
        nC = nI-nH
    return tF, nF, nR, nH, nC

print(f'''\
SIMULATION

tT (target temp)     = {tT:.2f}
pT (target pressure) = {pT:.2f}
nT (target moles)    = {moles(pT, vF, tT):.2f}

tF (furnace initial temp)     = {tF:.2f}
pF (furnace initial pressure) = {pF:.2f}
nF (furnace initial moles)    = {moles(pF, vF, tF):.2f}''')

nRs = 10
res = findSolution(Params(tT, pT, vF), Params(tF, pF, vF), tH, tC, nRs)

if res:
    tF, nF, nR, nH, nC = res
    nF -= nR
    nI = nH+nC
    tI = (tH*nH+tC*nC)/nI
    tF = (tF*nF+tI*nI)/(nF+nI)
    nF += nI
    pF = nF*R*tF/vF
    print(f'''
- (stepping up nR in {nRs:.2f} increments)
- Removing nR = {nR:.2f} moles
- Added nH = {nH:.2f} moles from H to I
- Added nC = {nC:.2f} moles from C to I
- I has temperature tI = {tI:.2f}
              moles nI = {nI:.2f}
- Added I to F
- Result temperature tF = {tF:.2f}
- Result pressure    pF = {pF:.2f}
''')
else:
    print('No solution')

