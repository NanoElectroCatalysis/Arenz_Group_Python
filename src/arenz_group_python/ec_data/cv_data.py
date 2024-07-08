""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import math
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import .ec_data as EC_Data


def CV(ecdata:EC_data)
####SPLITT
import numpy as np

    x = data[1].E
    y = data[1].i
    t = data[1].Time

    xmin = x.min()
    xmax = x.max()

    x_start = np.mean(x[0:3])
    index_min = np.argmin(x)
    index_max = np.argmax(x)


    x_div = np.gradient(x)
    zero_crossings = np.where(np.diff(np.signbit(x_div)))[0]

    up_start =0
    up_end = 0



    print(zero_crossings)
    if x[0]<x[zero_crossings[0]]:
        print("up")
        up_start =0
        up_end = zero_crossings[0]
        dn_start = zero_crossings[0]
        dn_end = x.size
    else:
        up_start =zero_crossings[0]
        up_end = x.size
        dn_start = 0
        dn_end = zero_crossings[0]
        
        

    x_u = x[0:zero_crossings[0]]
    y_u = y[0:zero_crossings[0]]
    x_n = np.flipud(x[zero_crossings[0]:])
    y_n = np.flipud(y[zero_crossings[0]:])
    x_sweep = np.linspace(-2.5, 2.5, 1000)
    y_up=np.interp(x_sweep, x_u, y_u)
    y_down=np.interp(x_sweep, x_n, y_n)

    for i in range(1,y_up.size):
        if y_up[i-1] == y_up[i]:
            y_up[i-1] = math.nan
        else :
            break
        
    for i in range(y_up.size-2,0,-1):
        if y_up[i] == y_up[i+1]:
            y_up[i+1] = math.nan
        else :
            break
        
    for i in range(1,y_down.size):
        if y_down[i-1] == y_down[i]:
            y_down[i-1] = math.nan
        else :
            break
        
    for i in range(y_down.size-2,0,-1):
        if y_down[i] == y_down[i+1]:
            y_down[i+1] = math.nan
        else :
            break