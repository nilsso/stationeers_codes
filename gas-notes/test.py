from random import random

R = 8.31446261815324
cp = 28.2 # CO2

def TAB(TA, nA, TB, nB):
    return (TA*nA+TB*nB)/(nA+nB)

def P(V, n, T):
    return n*R*T/V

# furnace (initial) conditions:
VF = 1000
PF0 = 50000
TF0 = 200
nF0 = (PF0*VF)/(R*TF0)
nF0_ = nF0
# furnace target conditions:
PF = 50000
TF = 400
# hot gas initial conditions:
VH = 5 * 100
# TH0 = 2500
TH0 = 2500 - random() * 250
# nH0 = 500
nH0 = 500 + random() * 2000
# PH0 = P(VH0, nH0, TH0)
# cold gas initial conditions:
VC = 5 * 100
TC0 = 200
# TC0 = 200 + random() * 100
nC0 = 500
# nC0 = 500 + random() * 2000
# PC0 = P(VC, vC, TC)

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
VALIDATING:

initial furnace conditions
TF0 = {TF0:.2f} K
PF0 = {PF0:.2f} kPa
nF0 = {nF0_:.2f} moles

expected results
TF = {TF:.2f}
PF = {PF:.2f}
''')

nI = nH + nC
TI = (TH0*nH+TC0*nC)/(nH+nC)
TF = (TI*nI+TF0*nF0)/(nI+nF0)
nF = nF0+nI
PF = nF*R*TF/VF

print(f'''\
initial conditions of H and C
TH0 = {TH0:.2f} K
nH0 = {nH0:.2f} moles
TC0 = {TC0:.2f} K
nC0 = {nH0:.2f} moles
''')

if nF0 != nF0_:
    print(f'''\
dumped {round(nF0_-nF0, 2)} moles from nF0
''')

print(f'''\
calculated moles H/C to compose
nH = {nH:.2f} moles
nC = {nC:.2f} moles

mixed {RH}%/{RC}% until {nI:.2f} moles

added composition to F0
nF (result) = {nF:.2f} moles = {nF0:.2f} + {nI:.2f} moles
TF (result) = {TF:.2f} K
PF (result) = {PF:.2f} kPa
''')



