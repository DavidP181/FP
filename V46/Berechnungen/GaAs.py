import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import scipy.constants as const
from scipy.optimize import curve_fit
from uncertainties import correlated_values, correlation_matrix
from uncertainties import ufloat
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
x = np.linspace(0, 3, 1000)
me= const.electron_mass
n=3.3543 # Brechungsindex für GaAs bei einer Wellenlänge von 1771.14
A= (const.e**3 *ufloat(0.436,0.008))  / ( 8*(np.pi**2) * const.epsilon_0*(const.c**3) *n)  #konst zum bestimmen der eff Masse
def mittel(x):              #the real mean()-ing of life
    return ufloat(np.mean(x),np.std(x,ddof=1)/np.sqrt(len(x)))
def relf(l,m):  #in Prozent
    return (np.absolute(l-m)/l)*100

# d = dicke= Länge im Strahlengang
hd = 5.11*10**-3
d1 = 1.296*10**-3
d2 = 1.36*10*10**-3
#Werte einlesen
lamda, rein_t1, rein_t2, N1_t1, N1_t2, N2_t1, N2_t2 = np.genfromtxt('Daten/Winkel.txt', unpack = True)

#Fehlerrechnung
rein_t1 = unp.uarray(rein_t1, 2)
rein_t2 = unp.uarray(rein_t2, 2)
N1_t1   = unp.uarray(N1_t1, 2)
N1_t2   = unp.uarray(N1_t2, 2)
N2_t1   = unp.uarray(N2_t1, 2)
N2_t2   = unp.uarray(N2_t2, 2)




#Umrechnen auf Meter, bzw. Bogenmaß
lamda = lamda * 10**(-3)
rein_t1 = rein_t1 /360
rein_t2 = rein_t2 /360
N1_t1   = N1_t1 /360
N1_t2   = N1_t2 /360
N2_t1   = N2_t1 /360
N2_t2   = N2_t2 /360

#Winkel
rein = 1/2 * (rein_t1 - rein_t2)
N1   = 1/2 * (N1_t1 - N1_t2)
N2   = 1/2 * (N2_t1 - N2_t2)
rein = abs(rein)
N1   = abs(N1)
N2   = abs(N2)

#Differenzzwischen der hochreinen und den zwei Proben
D1 = abs(rein/hd-N1/d1)
D2 = abs(rein/hd-N2/d2)

C1= A*2.8*10**16 #weil umgerechnet auf Meter
C2= A*1.2*10**16

#Fitfunktion
def fitf1(x,a,c):
	return x*a + c

print(lamda, D1, D2)
params , cov = curve_fit(fitf1 ,lamda**2,unp.nominal_values(D1))
params = correlated_values(params, cov)
params2 , cov2 = curve_fit(fitf1 ,lamda**2 ,unp.nominal_values(D2))
params2 = correlated_values(params2, cov2)


norm_rein = (rein/hd)
norm_N1 = (N1/d1)
norm_N2 = (N2/d2)



#Tabelle
np.savetxt('Tabellen/HGaAstab.txt',np.column_stack([(lamda*10**(-6)),unp.nominal_values(rein), unp.std_devs(rein), unp.nominal_values(norm_rein), unp.std_devs(norm_rein)]), delimiter=' & ',newline= r'\\'+'\n' )
np.savetxt('Tabellen/1.nGaAstab.txt',np.column_stack([(lamda*10**(-6)),unp.nominal_values(N1), unp.std_devs(N1), unp.nominal_values(norm_N1), unp.std_devs(norm_N1)]), delimiter=' & ',newline= r'\\'+'\n' )
np.savetxt('Tabellen/2.nGaAstab.txt',np.column_stack([(lamda*10**(-6)),unp.nominal_values(N2), unp.std_devs(N2), unp.nominal_values(norm_N2), unp.std_devs(norm_N2)]), delimiter=' & ',newline= r'\\'+'\n' )

#Plots
plt.plot(lamda**2 , unp.nominal_values(D1), 'ro', label= 'Differenz mit 1.8.n-dot')
plt.plot(lamda**2 , unp.nominal_values(D2), 'bo', label= 'Differenz mit 2.8.n-dot')
plt.plot(x**2,fitf1(x**2,unp.nominal_values(params2[0]),unp.nominal_values(params2[1])),'b--', label = 'Ausgleichsgerade für 2.8 n-dotiert')
plt.plot(x**2,fitf1(x**2, unp.nominal_values(params[0]), unp.nominal_values(params[1])),'r--', label = 'Ausgleichsgerade für 1.2 n-dotiert')
plt.xlabel(r'Wellenlänge zum Quadrat $\lambda^2 \:/\:\mu m^2 $')
plt.ylabel(r'Differenz der Längennormierten Winkel $\frac{\Delta\theta}{L} / \degree m^{-1} $')
plt.legend(loc='best')
plt.show()
plt.savefig('DeltaTheta.pdf')
