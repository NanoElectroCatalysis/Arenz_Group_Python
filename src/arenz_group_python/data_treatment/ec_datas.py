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
        
    def plot(self, x_channel:str, y_channel:str, *args, **kwargs):
        options = plot_options()
        options.update(kwargs)
        line, ax = options.exe()
        #ax = make_plot_1x(options.name)
        plot_kwargs = kwargs
        datas = copy.deepcopy(self.datas)
        for data in datas:
            plot_kwargs["plot"] = ax
            plot_kwargs["name"] = data.setup_data.name
            data.plot(x_channel, y_channel, **plot_kwargs)
        ax.legend()
        return ax