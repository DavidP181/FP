import numpy as np
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

R_p, R_r, I_p, U_p, I_r, U_r = np.genfromtxt('Daten/widerstand1.txt', unpack = True)
I_p = I_p * 0.001
t = np.zeros(32)
m = 0.342
rho = 8920
V_0 = m/rho
kappa = 443

def alpha(T):
    if(T<80): return 7.00
    if(80<T<90): return 8.50
    if(90<T<100): return 9.75
    if(100<T<110): return 10.70
    if(110<T<120): return 11.50
    if(120<T<130): return 12.10
    if(130<T<140): return 12.65
    if(140<T<150): return 13.10
    if(150<T<160): return 13.60
    if(160<T<170): return 13.90
    if(170<T<180): return 14.25
    if(180<T<190): return 14.50
    if(190<T<200): return 14.75
    if(200<T<210): return 14.95
    if(210<T<220): return 15.20
    if(220<T<230): return 15.40
    if(230<T<240): return 15.60
    if(240<T<250): return 15.75
    if(250<T<260): return 15.90
    if(260<T<270): return 16.10
    if(270<T<280): return 16.25
    if(280<T<290): return 16.35
    if(290<T<300): return 16.50
    if(300<T): return 16.65
    else: return 0


for i in range(0,31):
    t[i] = (i+1)*300


T = 0.00134 * R_p**2 + 2.296*R_p - 243.02 + 273.15
print(T)
x = np.zeros(32)
C_p = x
C_v = x

for i in range(1, 31):
    C_p[i] = (I_p[i-1] * U_p[i-1] * 300)/(m*(T[i]-T[i-1]))



for i in range(1, 31):
    C_v[i] = -9 * alpha(T[i])**2 * kappa * V_0 * T[i] + C_p[i]

def f(T, a, b):
    return a*T+b

param, cov = curve_fit(f, T, C_v)
print(*param)
T_test = np.linspace(80,300, 300)
print(C_v)
print(f(T, *param))
plt.plot(T, C_v, 'bx', label = 'Messung')
plt.plot(T_test, f(T_test, *param), 'r-', label = 'Regression')
plt.show()
