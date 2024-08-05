""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from . import util
from .util_graph import plot_options
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
    
    def __getitem__(self, item_index:int) -> EC_Data: 
        return self.datas[item_index]
    
    def __setitem__(self, item_index:int, new_data:EC_Data):
        self.datas[item_index] = new_data
        
    def plot(self, x_channel:str, y_channel:str, *args, **kwargs):
        fig = plt.figure()
            #  plt.subtitle(self.name)
        ax = fig.subplots()
        plot_kwargs = kwargs
        datas = copy.deepcopy(self.datas)
        for data in datas:
            plot_kwargs["plot"] = ax
            data.plot(x_channel, y_channel, **plot_kwargs)
        return ax