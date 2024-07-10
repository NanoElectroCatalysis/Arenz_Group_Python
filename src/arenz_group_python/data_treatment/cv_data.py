""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter 
from . import util
from .ec_data import EC_Data

from .ec_setup import EC_Setup
from .util import plot_options
from pathlib import Path
     


class CV_Data(EC_Setup):
    def __init__(self):
        super().__init__()
        #self._area=2
        #self._area_unit="cm^2"
        #self.rotation =0
        #self.rotation_unit ="/min"
        self.E=[]
        self.i_p=[]
        self.i_n=[]
        self.i_label = "i"
        self.i_unit = "A"
        self.rate_V_s = 1
        self.E_max = 2.5
        """max voltage""" 
        self.E_min = -2.5
        """min voltage"""
        self.name="CV"
        self.xmin = -2.5
        self.xmax = 2.5
        self.setup = {}
        
    def sub(self, subData):
        try:
            self.i_p = self.i_p-subData.i_p
            self.i_n = self.i_n-subData.i_n
        finally:
            return
        
    def div(self, div_factor:float):
        try:
            self.i_p = self.i_p / div_factor
            self.i_n = self.i_n / div_factor
        finally:
            return
    
    #def __add__(self, other):
    #    
    #    return "aa"
    
    def add(self, subData):
        try:
            self.i_p = self.i_p+subData.i_p
        finally:
            pass
        try:
            self.i_n= self.i_n+subData.i_n
        finally:
            pass
        return
        
    def smooth(self, smooth_width:int):
        try:
            self.i_p = savgol_filter(self.i_p, smooth_width, 1)
            self.i_n = savgol_filter(self.i_n, smooth_width, 1)     
        finally:
            return
    
    def set_area(self,value,unit):
        self._area = value
        self._area_unit = unit
    
    def conv(self, data: EC_Data):
        """Converts EC_Data to a CV

        Args:
            data (EC_Data): the data that should be converted.
        """
        self.convert(data.Time,data.E,data.i)
        self.setup = data.setup
        self.set_area(data._area, data._area_unit)
        self.set_rotation(data.rotation, data.rotation_unit)
        self.name = data.name
        return
        
    def convert(self, time, E, i, **kwargs):
        """Converts data to CV data

        Args:
            time (_type_): time
            E (_type_): potential
            i (_type_): current
            direction(str): direction
        """
        x= E
        y= i
        options = plot_options(kwargs)
        
        #try:
        #    y_smooth = int(options['y_smooth'])
        #    if(y_smooth > 0):
        #        y = savgol_filter(y, y_smooth, 1)
        #finally:
        #    pass
        
        y =options.smooth_y(y)
        
        self.xmin = x.min()
        self.xmax = x.max()

        x_start = np.mean(x[0:3])
        index_min = np.argmin(x)
        index_max = np.argmax(x)

        #array of dx
        x_div = np.gradient(x)
        #dt:
        t_div = (time.max() - time.min()) / (time.size - 1)
        zero_crossings = np.where(np.diff(np.signbit(x_div)))[0]
        
        self.rate_V_s = np.mean(np.abs(x_div)) / t_div
        #print(f"Rate: {self.rate_V_s}")
        up_start =0
        up_end = 0



        #print(f"ZeroCrossings: {zero_crossings}"")
        if x[0]<x[zero_crossings[0]]:
            up_start =0
            up_end = zero_crossings[0]
            dn_start = zero_crossings[0]
            dn_end = x.size
        else:
            up_start =zero_crossings[0]
            up_end = x.size
            dn_start = 0
            dn_end = zero_crossings[0]
        
        self.E_max = 2.5
        self.E_min = -2.5
        dE_range = int((self.E_max - self.E_min)*1000)
        x_sweep = np.linspace(self.E_min, self.E_max, dE_range) 
        self.E = x_sweep
        
        x_u = x[0:zero_crossings[0]]
        y_u = y[0:zero_crossings[0]]
        x_n = np.flipud(x[zero_crossings[0]:])
        y_n = np.flipud(y[zero_crossings[0]:])
        
        y_pos=np.interp(x_sweep, x_u, y_u)
        y_neg=np.interp(x_sweep, x_n, y_n)

        for i in range(1,y_pos.size):
            if y_pos[i-1] == y_pos[i]:
                y_pos[i-1] = math.nan
            else :
                break
            
        for i in range(y_pos.size-2,0,-1):
            if y_pos[i] == y_pos[i+1]:
                y_pos[i+1] = math.nan
            else :
                break
            
        for i in range(1,y_neg.size):
            if y_neg[i-1] == y_neg[i]:
                y_neg[i-1] = math.nan
            else :
                break
            
        for i in range(y_neg.size-2,0,-1):
            if y_neg[i] == y_neg[i+1]:
                y_neg[i+1] = math.nan
            else :
                break
            
        self.i_p = y_pos     
        self.i_n = y_neg
    
    
    def norm(self, norm_to:str):
        norm_factor = 1
        norm_label = ""
        norm_unit = ""
        if norm_to == "area" :
           norm_factor = self._area
           norm_label = "$A^{-1}$"
           norm_unit = self._area_unit
        elif norm_to == "rate" :
           norm_factor = self.rate_V_s
           norm_label = "$v^{-1}$"
           norm_unit = "s $V^{-1}$"
        elif norm_to == "sqrt_rate":
           norm_factor = math.sqrt(self.rate_V_s)
           norm_label = "$v^{-0.5}$"
           norm_unit = "$s^{0.5}$ $V^{-0.5}$"
        elif norm_to == "rot_rate":
           norm_factor = math.sqrt(self.rot_rate_Hz)
           norm_label = "$f^{-1}$"
           norm_unit = "$Hz^{-1}$"
          
        elif norm_to == "sqrt_rot_rate":
           norm_factor = math.sqrt(self.rot_rate_Hz)
           norm_label = "$f^{-0.5}$"
           norm_unit = "$Hz^{-0.5}$"    
        else:
            return
                
        self.i_n = self.i_n /norm_factor
        self.i_p = self.i_p /norm_factor
        self.i_label = self.i_label +" "+ norm_label
        self.i_unit = self.i_unit +" "+ norm_unit
        return 
    
            
    def plot(self,**kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot=subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        '''
        xlable ="wrong channel name"
        xunit = ""
        ylable ="wrong channel name"
        yunit = "wrong channel name"
       
        options = plot_options(kwargs)  
        
        
        xdata = self.E
        if(options.get_dir() == "pos"):  
            ydata = self.i_p
        
        elif(options.get_dir() == "neg"):  
             ydata = self.i_n
             
        else:
            xdata=np.concatenate((self.E, self.E), axis=None)
            ydata=np.concatenate((self.i_p, self.i_n), axis=None)  
        
        options.set_x_txt("E", "V")
        options.set_y_txt(self.i_label, self.i_unit)
        
        '''add a the data to an existing plot or create a new'''
        try:
            ax = kwargs['plot']     
        except:
            fig = plt.figure()
            plt.suptitle(self.name)
            ax = fig.subplots()
        #try:
        #    y_smooth = int(options['y_smooth'])
        #    if(y_smooth > 0):
        #        ydata = savgol_filter(ydata, y_smooth, 1)
        #except:
        #    pass
        ydata = options.smooth_y(ydata) 
        try:
            line, = ax.plot(xdata,ydata)
            line.set_label(options.get_legend())
        except:
            pass
        #ax.set_xlabel(f'{xlable} / {xunit}')
        #ax.set_ylabel(f'{ylable} / {yunit}')
        ax.set_ylabel(options.get_y_txt())
        ax.set_xlabel(options.get_x_txt())
        return ax
    
    def get_i_at_E(self, E:float, dir:str = "all"):
        """Get the current at a specific voltage.

        Args:
            E (float): potential where to get the current. 
            dir (str): direction, "pos,neg or all"
        Returns:
            _type_: _description_
        """
        index = 0
        for x in self.E:
            if x > E:
                break
            else:
                index = index + 1
                
        if dir == "pos":
            return self.i_p[index]
        elif dir == "neg":
            return self.i_n[index]
        else:
            return [self.i_p[index] , self.i_n[index]]
    
