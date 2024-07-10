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
from .cv_data import CV_Data
from .ec_setup import EC_Setup
from .util import plot_options
from pathlib import Path
import copy

class CV_Datas:
    def __init__(self, paths:list[Path]):
        
        self.datas = [CV_Data() for i in range(len(paths))]
        index=0
        for path in paths:
            ec = EC_Data(path)
            try:
                self.datas[index].conv(ec)
            finally:
                index=index+1 
        #print(index)
        return
    
    def Levich(self, Epot):
        fig = plt.figure()
        fig.set_figheight(5)
        fig.set_figwidth(10)
        plt.suptitle("Levich Analysis")
        CV_plot, analyse_plot = fig.subplots(1,2)
        analyse_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Levich Plot')
        
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        CVs = copy.deepcopy(self.datas)
        #CVs = [CV_Data() for i in range(len(paths))]
        for cv in CVs:
            rot.append(math.sqrt(cv._rotation))
        
            cv.norm("area")
            cv.plot(plot = CV_plot, legend = cv._rotation)
            y.append(cv.get_i_at_E(Epot))
            E.append([Epot, Epot])
            y_axis_title= cv.i_label
            #print(cv.setup)
        #print(rot)
        rot = np.array(rot)
        y = np.array(y)
        CV_plot.plot(E,y, "o")
        CV_plot.legend()
        #print(rot)
        #print(y[:,0])

        analyse_plot.plot(rot,y,'o')

        analyse_plot.set_xlabel("rotation$^{0.5}$")
        analyse_plot.set_ylabel(y_axis_title)
        m_pos, b = np.polyfit(rot, y[:,0], 1)
        y_pos= m_pos*rot+b
        line,=analyse_plot.plot(rot,y_pos,'-' )
        line.set_label(f"pos: m={m_pos:3.3e}")
        m_neg, b = np.polyfit(rot, y[:,1], 1)
        y_neg= m_neg*rot+b
        line,=analyse_plot.plot(rot,y_neg,'-' )
        line.set_label(f"neg: m={m_neg:3.3e}")
        analyse_plot.legend()
        return m_pos,m_neg

    def KouLev(self, Epot):
        fig = plt.figure()
        fig.set_figheight(5)
        fig.set_figwidth(10)
        plt.suptitle("Koutechy-Levich Analysis")
        CV_plot, analyse_plot = fig.subplots(1,2)
        CV_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Koutechy-Levich Plot')
        
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        CVs = copy.deepcopy(self.datas)
        for cv in CVs:
            rot.append( math.sqrt(cv._rotation))
        
            cv.norm("area")
            cv.plot(plot = CV_plot, legend = cv._rotation)
            y.append(cv.get_i_at_E(Epot))
            E.append([Epot, Epot])
            y_axis_title= cv.i_label
            #print(cv.setup)
        #print(rot)
        CV_plot.plot(E,y, "o")
        CV_plot.legend()
        
        rot = np.array(rot) 
        rot = 1 / rot    
        y_values = np.array(y)
        y_inv = 1/ y_values

        #print(rot)
        #print(y[:,0])

        analyse_plot.plot(rot,y_inv,'o')

        analyse_plot.set_xlabel("rotation$^{0.5}$")
        analyse_plot.set_ylabel(y_axis_title)
        m_pos, b = np.polyfit(rot, y_inv[:,0], 1)
        y_pos= m_pos*rot+b
        line,=analyse_plot.plot(rot,y_pos,'-' )
        line.set_label(f"pos: m={m_pos:3.3e}")
        m_neg, b = np.polyfit(rot, y_inv[:,1], 1)
        y_neg= m_neg*rot+b
        line,=analyse_plot.plot(rot,y_neg,'-' )
        line.set_label(f"neg: m={m_neg:3.3e}")
        analyse_plot.legend()
        return m_pos,m_neg
    
    def Tafel(self, Epot):
        fig = plt.figure()
        fig.set_figheight(5)
        fig.set_figwidth(10)
        plt.suptitle("Tafel Analysis")
        CV_plot, analyse_plot = fig.subplots(1,2)
        CV_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Tafel Plot')
        
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        CVs = copy.deepcopy(self.datas)
        for cv in CVs:
            rot.append( math.sqrt(cv._rotation))
        
            cv.norm("area")
            cv.plot(plot = CV_plot, legend = cv._rotation)
            y.append(cv.get_i_at_E(Epot))
            E.append([Epot, Epot])
            y_axis_title= cv.i_label
            #print(cv.setup)
        #print(rot)
        CV_plot.plot(E,y, "o")
        CV_plot.legend()
        
        rot = np.array(rot) 
        rot = 1 / rot    
        y_values = np.array(y)
        y_inv = 1/ y_values

        #print(rot)
        #print(y[:,0])

        analyse_plot.plot(rot,y_inv,'o')

        analyse_plot.set_xlabel("rotation$^{0.5}$")
        analyse_plot.set_ylabel(y_axis_title)
        m_pos, b = np.polyfit(rot, y_inv[:,0], 1)
        y_pos= m_pos*rot+b
        line,=analyse_plot.plot(rot,y_pos,'-' )
        line.analyse_plot(f"pos: m={m_pos:3.3e}")
        m_neg, b = np.polyfit(rot, y_inv[:,1], 1)
        y_neg= m_neg*rot+b
        line,=analyse_plot.plot(rot,y_neg,'-' )
        line.set_label(f"neg: m={m_neg:3.3e}")
        analyse_plot.legend()
        return m_pos,m_neg
     