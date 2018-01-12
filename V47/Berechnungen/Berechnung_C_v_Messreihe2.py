#Berechnungen für den zweiten Datensatz für die Debye-Temperatur
import numpy as np
import uncertainties.unumpy as unp
from uncertainties import ufloat
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

R_p, err_Rp, R_r, err_Rr, I_p, err_Ip, U_p, err_Up, I_r, U_r = np.genfromtxt('Daten/widerstand2.txt', unpack = True)
T_a, alpha_2 = np.genfromtxt('Daten/alpha.txt', unpack = True)
alpha_2 = alpha_2 * 10**(-6)
T_a = T_a + 273.15
#I_p = I_p * 0.001
t = np.zeros(32)
err_t = np.zeros(32)
m = 0.342
rho = 8920
V_0 = m/rho
kappa = 443
M = 63.55
n = 342/M
for i in range(0,20):
    t[i] = (i+1)*300
    err_t[i] = 5

R_p = unp.uarray(R_p, err_Rp)
R_r = unp.uarray(R_r, err_Rr)
t = unp.uarray(t, err_t)
U_p = unp.uarray(U_p, err_Up)
I_p = unp.uarray(I_p, err_Ip)

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






T = 0.00134 * R_p**2 + 2.296*R_p - 243.02 + 273.15
T2 = 0.00134 * R_r**2 + 2.296*R_r - 243.02 + 273.

#print('Temperatur Probe in K: ')
#print(T)
x = np.zeros(32)
C_p = unp.uarray(x,x)
C_v = unp.uarray(x,x)

#print('Nummer i des Messintervalls, C_p[i], TempErhöhung, eingewirkte Stromstärke, eingewirkte Spannung, n: ')
for i in range(1, 20):
   C_p[i] = (I_p[i-1] * U_p[i-1] * 300)/(n*(T[i]-T[i-1]))
#    print(i, C_p[i], T[i]-T[i-1], I_p[i-1], U_p[i-1], n)


#print(T[i]-T[i-1])

#print('Temperatur Probe in K: ')
#print(T)
#print('Temperatur Kupferrohr: ')
#print(T2)
#print('C_v: ')
for i in range(1, 20):
    C_v[i] = -9 * a_func(T[i], *param_a)**2 * kappa * V_0 * T[i] + C_p[i]
    a= -9 * a_func(T[i], *param_a)**2 * kappa * V_0 * T[i]
#print(C_v[14])


def debyetemp(ym, yp, xm, xp, T, C_v):
    return (xp + (C_v-yp)*(xm-xp)/(ym-C_v))*T

#ym = 24.5
#yp = 24.63
#xm = 0.5
#xp = 0.6
#x = xp + (C_v[15]-yp)*(xm-xp)/(ym-C_v[15])
#T = ufloat(155.58, 0.24)
#print(x*T)
theta1 = debyetemp(18.6, 18.8, 2.5, 2.6, T[0], C_v[1]  )
theta14 = debyetemp(23.74, 23.96, 1, 1.1, T[13], C_v[14]  )
theta15 = debyetemp(24.5, 24.63, 0.5, 0.6, T[14], C_v[15]  ) # unp.nominal_values(y) gibt nur den Wert von y aus , yerr = unp.std_devs(y)
#print(theta1, T[0], C_v[1])
#print(theta14, T[13], C_v[14])
#print(theta15, T[14], C_v[15])
#unp.mean(theta1, theta14, theta15)
#print(mean)
Mittelwert= ((210/200**2)+(100/6700**2)+(90/830**2))/(1/200**2+1/6700**2+1/830**2)
print('Mittelwert')
print(Mittelwert)
