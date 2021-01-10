% All gas model
% global R;
R = 8.31446261815324;
global c;
global nF0;
global rF;
global nH0;
global rH;
global nC0;
global rC;

c =  [
    20.4 % H2 (hydrogen)
    20.6 % N2 (nitrogen)
    21.1 % O2 (oxygen)
    24.8 % X (pollutant)
    28.2 % CO2 (carbon-dioxide)
    72.0 % H2O (water)
    23.0 % N2O (nitrous-oxide)
    ];

% Hot source
tH = 2300;
nH0 = 1000;
rH = [
    0.018121911037891267 % H2
    0.0                  % N2
    0.004942339373970346 % O2
    0.317957166392092260 % X
    0.658978583196046100 % CO2
    0.0                  % H2O
    0.0                  % N2O
    ];
sH = dot(rH, c);

% Cold source
tC = 300;
nC0 = 1000;
rC = [
    0.0  % H2
    0.03 % N2
    0.01 % O2
    0.01 % X
    0.95 % CO2
    0.0  % H2O
    0.0  % N2O
    ];
sC = dot(rC, c);

% Furnace (initial)
vF = 1000;
tF = 600;
pF0 = 1000;
nF0 = moles(pF0, vF, tF);
rF = rH;
sF = dot(rH, c);

tT = 1300; % Temperature target
pT = 10000; % Pressure target

visualize(31);
             
function sT = calc_sT(gamma, alpha, beta)
    global c;
    global nF0;
    global rF;
    global nH0;
    global rH;
    global nC0;
    global rC;
    
    w = size(alpha, 1);
    h = size(alpha, 2);
    
    nF = gamma*nF0.*repmat(reshape(rF, 1, 1, 7), w, h);
    nH = alpha*nH0.*repmat(reshape(rH, 1, 1, 7), w, h);
    nC = beta *nC0.*repmat(reshape(rC, 1, 1, 7), w, h);
    nT = nF+nH+nC;
    
    sT = dot(nT, repmat(reshape(c, 1, 1, 7), w, h), 3);
end

% Calculate moles
function n = moles(p, v, t)
    global R;
    n = (p*v)/(R*t);
end

function s = heatCapacity(varargin)
    global c;
    a = sum(cell2mat(varargin), 2);
    s = dot(a/sum(a), c);
end

function [] = visualize(w)
    x = linspace(0, 1, w);
    [alpha, beta] = meshgrid(x, x);
    gamma = 0.0;
    
    S.fh = figure(...
        'units','pixels', 'position',[300 300 300 300],...
        'menubar','none',...
        'name','slider_plot',...
        'numbertitle','off');
    
    S.ax = axes('units', 'pixels', 'position',[30 90 260 200]);
    S.gamma = gamma;
    S.alpha = alpha;
    S.beta = beta;
    S.sT = calc_sT(S.alpha, S.beta, S.gamma);
    S.plot = surf(S.alpha, S.beta, S.sT);
    update(S);

    S.gammaSlider = uicontrol(...
        'style','slider',...
        'unit','pixels',...
        'position',[20 10 260 20],...
        'min',0,'max',1,'value', S.gamma,...
        'sliderstep',[1/20 1/20],...
        'callback', {@GammaSlider, 'gamma'});
    
    guidata(S.fh, S);
end

function GammaSlider(Slider, EventData, Param)
    S = guidata(Slider);
    S.(Param) = get(Slider, 'Value');
    update(S);
    guidata(Slider, S);
end

function [] = update(S)
    set(S.plot, 'ZData', calc_sT(S.alpha, S.beta, S.gamma));
end








