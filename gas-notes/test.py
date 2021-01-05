from random import random

R = 8.31446261815324
cp = 28.2 # CO2

def TAB(TA, nA, TB, nB):
    return (TA*nA+TB*nB)/(nA+nB)

def P(V, n, T):
    return n*R*T/V

VF = 1000

# TF0 = 300
# nF0 = 30
# PF = 10000
# TF = 1000
# TH0 = 2200
# nH0 = 2000
# TC0 = 200
# nC0 = 2000

try:
    TF0
except:
    TF0 = 300 + random() * 1500
    nF0 = 200 + random() * 200
    PF = random() * 50000
    TF = 300 + random() * 1500
    TH0 = 2500 - random() * 250
    nH0 = 100 + random() * 100
    TC0 = 200 + random() * 100
    nC0 = 100 + random() * 100

nF0_ = nF0

print(f'''\
TH0 (H initial temp)  = {TH0:.2f} K
nH0 (H initial moles) = {nH0:.2f} moles
TC0 (C initial temp)  = {TC0:.2f} K
nC0 (C initial moles) = {nC0:.2f} moles

TF0 (F initial temp)     = {TF0:.2f} K
PF0 (F initial pressure) = {P(VF, nF0, TF0):.2f} kPa
nF0 (F initial moles)    = {nF0:.2f} moles

TF (target temperature) = {TF:.2f} K
PF (target pressure)    = {PF:.2f} kPa

---
SIMULATION''')

# calculate moles to add/remove, and temperature to add

global nF
global nI
global TI
global nH
global nC

def calcMolesCandH():
    global nF
    global nI
    global TI
    global nH
    global nC
    nF = (PF*VF)/(R*TF)
    nI = nF - nF0
    TI = (TF*nF-TF0*nF0)/nI
    print(f'''
    Target moles      : nF = {nF:.2f}
    Initial moles     : nF0 = {nF0:.2f}
    Moles to add      : nI = {nI:.2f}
    Input temperature : TI = {TI:.2f}
    ''')
    # compose input mixture
    nH = nI*(TI-TC0)/(TH0-TC0)
    # nH = min(100, max(0, nI*(TI-TC0)/(TH0-TC0)))
    nC = nI - nH
    # nC = nI*(TI-TH0)/(TC0-TH0)
    print(f'''\
    H moles to add : nH = {nH:.2f} moles
    C moles to add : nC = {nC:.2f} moles
    ''')

calcMolesCandH()
while min(nH, nC) < 0:
    m = min(nH, nC)
    print(f'(Dumped {-m:.2f} moles from furnace, then recalculated)')
    nF0 -= m
    calcMolesCandH()

nH = max(0, nH)
nC = max(0, nC)

print(nH, nC)

rH = nH/nH0
rC = nC/nC0

RH = round(rH/(rH+rC) * 100)
RC = 100 - RH
print(f'''\
H moles ratio : rH = nH/nH0 = {rH:.2f}
C moles ratio : rC = nC/nC0 = {rC:.2f}

H mixer setting : RH = round(rH/(rH+rC)*100) = {RH}%
C mixer setting : RC = 100 - RH = {RC}%

---
VALIDATING

nI = nH + nC = {nH:n} + {nC:n} = {nI:n}
TI = (TH0*nH+TC0*nC)/nI = {(TH0*nH+TC0*nC)/nI:n}
nF = nF0 + nI = {nF0:n} + nI = {nF0+nI:n}
TF = (TF0*nF0+TI*nI)/(nF0+nI) = {(TF0*nF0+TI*nI)/(nF0+nI):n}
PF = nF*R*TF/VF = {nF*R*TF/VF:n}''')



