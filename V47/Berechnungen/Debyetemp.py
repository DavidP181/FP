import numpy as np
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

T, err_T, C_v, err_C_v = np.genfromtxt('Daten/C_v_Temp.txt', unpack = True)
