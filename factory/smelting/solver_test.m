syms t_C t_H t_T t_F t_I
syms s_T s_F s_I s_R

conds = [
    (t_C < t_T) & (t_T < t_H)
    (t_C < t_F) & (t_F < t_H)
    (t_C < t_I) & (t_I < t_H)
    0 <= s_I
    (0 <= s_R) & (s_R <= s_F)
];

eqs = [
    t_T*s_T == t_F*(s_F-s_R)+t_I*s_I
    s_T == s_F-s_R+s_I
];

ineqs = [
    t_C*s_I <= t_I*s_I
];

all = cat(1, conds, eqs, ineqs);

sol = solve(all, [s_R; s_I], 'ReturnConditions', true);

sol.s_R
sol.s_I
sol.conditions