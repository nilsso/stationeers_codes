from random import random

R = 8.31446261815324
cp = 28.2 # CO2

def TAB(TA, nA, TB, nB):
    return (TA*nA+TB*nB)/(nA+nB)

def P(V, n, T):
    return n*R*T/V

VF = 1000
VH = 5 * 100
VC = 5 * 100

TF0 = 284.69
PF0 = 3799.38
nF0 = 1605.11

TF = 1728.95
PF = 1708.81

TH0 = 2356.82
nH0 = 1300.15
TC0 = 250.54
nC0 = 1300.15

if not TF0:
    # furnace (initial) conditions:
    # PF0 = 50000
    PF0 = random() * 50000
    # TF0 = 200
    TF0 = random() * 1800
    nF0 = (PF0*VF)/(R*TF0)
    # furnace target conditions:
    # PF = 50000
    PF = random() * 50000
    # TF = 400
    TF = random() * 1800
    # hot gas initial conditions:
    # TH0 = 2500
    TH0 = 2500 - random() * 250
    # nH0 = 500
    nH0 = 500 + random() * 2000
    # PH0 = P(VH0, nH0, TH0)
    # cold gas initial conditions:
    # TC0 = 200
    TC0 = 200 + random() * 100
    # nC0 = 500
    nC0 = 500 + random() * 2000
    # PC0 = P(VC, vC, TC)

nF0_ = nF0

print(f'''\
TF (target temperature) : TF = {TF:.2f} K
PF (target pressure)    : PF = {PF:.2f} kPa

H initial conditions : TH0 = {TH0:.2f} K, nH0 = {nH0:.2f} moles
C initial conditions : TC0 = {TC0:.2f} K, nC0 = {nC0:.2f} moles

Furnace initial conditions : TF0 = {TF0:.2f} K, PF0 = {PF0:.2f} kPa, nF0 = {nF0:.2f} moles

---
SIMULATION''')

# calculate moles to add/remove, and temperature to add
nF = (PF*VF)/(R*TF)
nI = nF - nF0
TI = (TF*nF-TF0*nF0)/nI
print(f'''
Target moles      : nF = {nF:.2f}
Initial moles     : nF0 = {nF0:.2f}
Moles to add      : nI = nF - nF0 = {nI:.2f}
Input temperature : TI = {TI:.2f}
''')


# compose input mixture
nH = nI*(TI-TC0)/(TH0-TC0)
# nH = min(100, max(0, nI*(TI-TC0)/(TH0-TC0)))
nC = nI - nH

print(f'''\
(Initial nH/nC calculation)
H moles to add : nH = {nH:.2f} moles
C moles to add : nC = nI - nH = {nC:.2f} moles
''')

# if False:
nHCmin = min(nH, nC)
if nHCmin < 0:
    nF0 += nHCmin
    nI = nF - nF0
    TI = (TF*nF-TF0*nF0)/nI
    nH = max(0, nI*(TI-TC0)/(TH0-TC0))
    nC = max(0, nI - nH)
    print(f'''\
(Dumped {-nHCmin:.2f} moles from furnace, then recalculated)
nF0 = {nF0:.2f}
nI = {nI:.2f}
TI = {TI:.2f}
nH = {nH:.2f}
nC = {nC:.2f}
''')

nH = max(0, nH)
nC = max(0, nC)

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



