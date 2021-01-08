R = 8.314;

vF = 1000; % Furnace volume
vS = 1500; % Hot/cold source volume
vI = 15000; % Input volume

% Initial conditions
% (Furnace)
tF0 = 500;
pF0 = 1000;
nF0 = moles(pF0, vF, tF0);
% (Hot source)
tH0 = 2300;
pH0 = 50000;
nF0 = moles(pH0, vS, tH0);
% (Cold source)
tC0 = 200;
pC0 = 10000;
nC0 = moles(pC0, vS, tC0);
% (Target)
tT = 1200;
pT = 20000;
nT = moles(pT, vF, tT);

N = 50;
[nR, tI] = meshgrid(0:(nF0-0)/N:nF0, tC0:(tH0-tC0)/N:tH0);
nI = (tT*nT-tF0.*(nF0-nR))./tI;

%surf(nR, tI, nI);

fig = uifigure;
sld = uislider(fig);

function n = moles(p, v, t)
    n = (p*v)/(8.314*t);
end