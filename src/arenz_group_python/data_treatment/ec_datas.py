""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from . import util
from .util_graph import plot_options,make_plot_1x
from .ec_setup import EC_Setup
from .ec_data import EC_Data
from pathlib import Path
import copy


class EC_Datas:
    def __init__(self, paths:list[Path], **kwargs):
        
        self.datas = [EC_Data() for i in range(len(paths))]
        index=0
        for path in paths:
            try:
                self.datas[index]=EC_Data(path)
            finally:
                index=index+1 
        #print(index)
        return
    
        
    def __getitem__(self, item_index:slice|int) -> EC_Data: 

        if isinstance(item_index, slice):
            step = 1
            start = 0
            stop = len(self.datas)
            if item_index.step:
                step =  item_index.step
            if item_index.start:
                start = item_index.start
            if item_index.stop:
                stop = item_index.stop    
            return [self.datas[i] for i in range(start,stop,step)  ]
        else:
            return self.datas[item_index]
    
    def __setitem__(self, item_index:int, new_data:EC_Data):
        if not isinstance(item_index, int):
            raise TypeError("key must be an integer")
        self.datas[item_index] = new_data
        
    def plot(self, x_channel:str = "E", y_channel:str = "i", *args, **kwargs):
        p = plot_options(kwargs)
        #options.update(kwargs)
        p.set_title("Data plot")
        line, ax = p.exe()
        #ax = make_plot_1x(options.name)
        plot_kwargs = kwargs
        datas = copy.deepcopy(self.datas)
        for data in datas:
            plot_kwargs["plot"] = ax
            plot_kwargs["name"] = data.setup_data.name
            plot_kwargs["legend"] = data.setup_data.name
            data.plot(x_channel, y_channel, **plot_kwargs)
        ax.legend()
        return ax
    
    def Tafel(self, x_channel:str = "i", y_channel:str = "E", transpose: bool = True, *args, **kwargs):
        
        plot_kwargs = kwargs

        if transpose:
           # t = x_channel
           # x_channel =y_channel
           # y_channel = t
            plot_kwargs["xscale"] ="log"
        else:
            plot_kwargs["yscale"] ="log"
             
        p = plot_options(kwargs)
        p.set_title("Tafel plot")
        #options.update(kwargs)
        
        line, ax = p.exe()
        #ax.set_yscale('log')
        #ax.get_yscale
        #ax = make_plot_1x(options.name)
        plot_kwargs["plot"] = ax        
        datas = copy.deepcopy(self.datas)
        #print("aaaaa", x_channel)
        for data in datas:
            plot_kwargs["name"] = data.setup_data.name
            plot_kwargs["legend"] = data.setup_data.name
            data.plot(x_channel, y_channel, **plot_kwargs)
        ax.legend()
        return ax