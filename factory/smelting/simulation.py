from random import random

R = 8.31446261815324
cp = 28.2 # CO2

# pv=nRt

def P(v, n, t):
    return (n*R*t)/v

def V(p, n, t):
    return (n*R*t)/p

def N(p, v, t):
    return (p*v)/(R*t)

def T(p, v, n):
    return (p*v)/(n*R)

def ta(na, tb, nb, tc, nc):
    return (tc*nc-tb*nb)/na

vF = 1000
vI = 1500
vH = 500
vC = 500

tH = 100
nH = 100

tC = 1
nC = 100

tF = 10
nF = 12

tT = 10
nT = 10

nD = 0

# print(nF)
print(nF-tT*nT/tF)

if nF >= nT:
    nF = tT*nT/tF

# print(nF)

# nI = nT-nF
# tI = (tT*nT-tF*nF)/nI
# nH = nI*(tI-tC)/(tH-tC)
# nC = nI-nH