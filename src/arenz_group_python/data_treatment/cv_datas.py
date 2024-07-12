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
    def __init__(self, paths:list[Path], **kwargs):
        
        self.datas = [CV_Data() for i in range(len(paths))]
        index=0
        for path in paths:
            ec = EC_Data(path)
            try:
                self.datas[index].conv(ec,**kwargs)
            finally:
                index=index+1 
        #print(index)
        return
    
    def __getitem__(self, item_index:int): 
        return self.datas[item_index]
    
    def __setitem__(self, item_index:int, new_CV:CV_Data):
        self.datas[item_index].new_CV
    
    def bg_corr(self, bg_cv:CV_Data):
        """Background correct the data by subtracting the bg_cv. 

        Args:
            bg_cv (CV_Data): _description_
        """
        for cv in self.datas:
            cv.sub(bg_cv)
        return copy.deepcopy(self)
    
    
    def _make_plot(self, Title:str):
        fig = plt.figure()
        fig.set_figheight(5)
        fig.set_figwidth(12)
        plt.suptitle(Title)
        CV_plot, analyse_plot = fig.subplots(1,2)
        return CV_plot, analyse_plot
    
    def Levich(self, Epot, *args):
        """Levich analysis. Creates plot of the data and a Levich plot.

        Args:
            Epot (_type_): Potential at which the current will be used.

        Returns:
            _type_: _description_
        """
  
        CV_plot, analyse_plot = self._make_plot("Levich Analysis")
        #CV_plot, analyse_plot = fig.subplots(1,2)
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
            rot.append(math.sqrt(cv.rotation))
            for arg in args:
                cv.norm(arg)
            cv.plot(plot = CV_plot, legend = cv.rotation)
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

        analyse_plot.set_xlabel("$\omega^{0.5}$ ( rpm$^{0.5}$)")
        analyse_plot.set_ylabel(y_axis_title)
        m_pos, b = np.polyfit(rot, y[:,0], 1)
        y_pos= m_pos*rot+b
        line,=analyse_plot.plot(rot,y_pos,'-' )
        line.set_label(f"pos: B={m_pos:3.3e}")
        m_neg, b = np.polyfit(rot, y[:,1], 1)
        y_neg= m_neg*rot+b
        line,=analyse_plot.plot(rot,y_neg,'-' )
        line.set_label(f"neg: B={m_neg:3.3e}")
        analyse_plot.legend()
        print("Levich", m_pos,m_neg)
        return m_pos,m_neg

    def KouLev(self, Epot, *args):
        #fig = plt.figure()
        #fig.set_figheight(5)
        #fig.set_figwidth(12)
        #plt.suptitle("Koutechy-Levich Analysis")
        CV_plot, analyse_plot = self._make_plot("Koutechy-Levich Analysis")
        
        #CV_plot, analyse_plot = fig.subplots(1,2)
        CV_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Koutechy-Levich Plot')
        
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        y_axis_unit =""
        CVs = copy.deepcopy(self.datas)
        for cv in CVs:
            rot.append( math.sqrt(cv.rotation))
            for arg in args:
                cv.norm(arg)
            cv.plot(plot = CV_plot, legend = cv.rotation)
            y.append(cv.get_i_at_E(Epot))
            E.append([Epot, Epot])
            y_axis_title= cv.i_label
            y_axis_unit= cv.i_unit
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

        analyse_plot.set_xlabel(str("$\omega^{-0.5}$" + "("+ "rpm$^{-0.5}$" +")"))
        analyse_plot.set_ylabel(str( f"(1 / ({y_axis_title}) +( 1 /{y_axis_unit})"))
        m_pos, b = np.polyfit(rot, y_inv[:,0], 1)
        y_pos= m_pos*rot+b
        B_pos = 1/m_pos
        line,=analyse_plot.plot(rot,y_pos,'-' )
        line.set_label(f"pos: m={B_pos:3.3e}")
        m_neg, b = np.polyfit(rot, y_inv[:,1], 1)
        y_neg= m_neg*rot+b
        B_neg = 1/m_neg
        line,=analyse_plot.plot(rot,y_neg,'-' )
        line.set_label(f"neg: m={B_neg:3.3e}")
        analyse_plot.legend()
        print("KouLev", B_pos,B_neg)
        return m_pos,m_neg
    
    def Tafel(self, E_for_idl:float, lims=[0,0], *args):
        """_summary_

        Args:
            E_for_idl (float): potential that used to determin the diffusion limited current.
            lims (list, optional): _description_. Defaults to [0,0].
        """
        CV_plot, analyse_plot = self._make_plot("Tafel Analysis")
        CV_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Tafel Plot')
        
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        CVs = copy.deepcopy(self.datas)
        for cv in CVs:
            rot.append( math.sqrt(cv.rotation))
        
            for arg in args:
                if arg == "area":
                    cv.norm(arg)
            cv.plot(plot = CV_plot, legend = cv.rotation)
            #.get_color()
            #color = line.get_color()
            i_dl_p,i_dl_n = cv.get_i_at_E(E_for_idl)
            y.append(cv.get_i_at_E(E_for_idl))
            xmin = cv.get_index_of_E(min(lims))
            xmax = cv.get_index_of_E(max(lims))
            #y_data = cv.i_p[xmin:xmax]
            y_data = [math.log10(abs(1/(1/i-1/i_dl_p))) for i in cv.i_p]
            m_pos, b = np.polyfit(cv.E[xmin:xmax], y_data[xmin:xmax], 1)
            y_pos= m_pos*cv.E[xmin:xmax]+b
            print("Tafel", 1./ m_pos , "V/dec")
            E.append([E_for_idl, E_for_idl])
            y_axis_title= cv.i_label
            analyse_plot.plot(cv.E, y_data)
            line, = analyse_plot.plot(cv.E[xmin:xmax], y_pos)
            line.set_label(f"pos: m={1000/m_pos:3.1f}mV/dec")
            #print(cv.setup)
        #print(rot)
        
        CV_plot.plot(E,y, "o")
        CV_plot.legend()
        
        rot = np.array(rot) 
        rot = 1 / rot    
        y_values = np.array(y)
        y_inv = 1/ y_values

        analyse_plot.set_xlim(lims[0]-0.1,lims[1]+0.1)
        #print(rot)
        #print(y[:,0])

        #analyse_plot.plot(rot,y_inv,'o')

        analyse_plot.set_xlabel("E / V")
        analyse_plot.set_ylabel(f"log( {y_axis_title} / {y_axis_title})" )
        #m_pos, b = np.polyfit(rot, y_inv[:,0], 1)
        #y_pos= m_pos*rot+b
        #line,=analyse_plot.plot(rot,y_pos,'-' )
        #line.set_label(f"pos: m={m_pos:3.3e}")
        #m_neg, b = np.polyfit(rot, y_inv[:,1], 1)
        #y_neg= m_neg*rot+b
        #line, = analyse_plot.plot(rot,y_neg,'-' )
        #line.set_label(f"neg: m={m_neg:3.3e}")
        analyse_plot.legend()
        #print("Tafel",m_pos,m_neg)
        #return m_pos,m_neg
     