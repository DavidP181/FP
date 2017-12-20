import numpy as np
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

R_p, R_r, I_p, U_p, I_r, U_r = np.genfromtxt('Daten/widerstand1.txt', unpack = True)
T_a, alpha_2 = np.genfromtxt('Daten/alpha.txt', unpack = True)
alpha_2 = alpha_2 * 10**(-6)
T_a = T_a + 273.15
I_p = I_p * 0.001
t = np.zeros(32)
m = 0.342
rho = 8920
V_0 = m/rho
kappa = 443
M = 63.55
n = 342/M

def a_func(T, a, b, c, d, e):
    return a*T**4+b*T**3+c*T**2+d*T+e
param_a, cov_a = curve_fit(a_func, T_a, alpha_2)
##def alpha(T):
#    if(T<80): return 7.00 * 10**(-6)
#    if(80<T<90): return 8.50 * 10**(-6)
#    if(90<T<100): return 9.75 * 10**(-6)
#    if(100<T<110): return 10.70 * 10**(-6)
#    if(110<T<120): return 11.50 * 10**(-6)
#    if(120<T<130): return 12.10 * 10**(-6)
#    if(130<T<140): return 12.65 * 10**(-6)
#    if(140<T<150): return 13.10 * 10**(-6)
#    if(150<T<160): return 13.60 * 10**(-6)
#    if(160<T<170): return 13.90 * 10**(-6)
#    if(170<T<180): return 14.25 * 10**(-6)
#    if(180<T<190): return 14.50 * 10**(-6)
#    if(190<T<200): return 14.75 * 10**(-6)
#    if(200<T<210): return 14.95 * 10**(-6)
#    if(210<T<220): return 15.20 * 10**(-6)
#    if(220<T<230): return 15.40 * 10**(-6)
#    if(230<T<240): return 15.60 * 10**(-6)
#    if(240<T<250): return 15.75 * 10**(-6)
#    if(250<T<260): return 15.90 * 10**(-6)
#    if(260<T<270): return 16.10 * 10**(-6)
#    if(270<T<280): return 16.25 * 10**(-6)
#    if(280<T<290): return 16.35 * 10**(-6)
#    if(290<T<300): return 16.50 * 10**(-6)
#    if(300<T): return 16.65 * 10**(-6)
#    else: return 0


for i in range(0,31):
    t[i] = (i+1)*300


T = 0.00134 * R_p**2 + 2.296*R_p - 243.02 + 273.15
print(T)
x = np.zeros(32)
C_p = x
C_v = x

for i in range(1, 31):
    C_p[i] = (I_p[i-1] * U_p[i-1] * 300)/(n*(T[i]-T[i-1]))
    print(i, C_p[i], T[i]-T[i-1], I_p[i-1], U_p[i-1], n)


print(T[i]-T[i-1])

for i in range(1, 31):
    C_v[i] = -9 * a_func(T[i], *param_a)**2 * kappa * V_0 * T[i] + C_p[i]
    a= -9 * a_func(T[i], *param_a)**2 * kappa * V_0 * T[i]
    print(a)


np.savetxt('Tabellen/C_V_und_C_P.txt', np.column_stack([t, C_v, C_p]))

def f(T, a, b):
    return a*T+b

param, cov = curve_fit(f, T[15:31], C_v[15:31])
print(*param)
T_test = np.linspace(150,300, 300)
#print(C_v)
#print(f(T, *param))
plt.plot(T[15:31], C_v[15:31], 'bx', label = 'Messung')
plt.plot(T_test, f(T_test, *param), 'r-', label = 'Regression')
plt.savefig('Bilder_Plots/plot1.pdf')
