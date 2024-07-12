""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from . import util
from .util import plot_options
from .ec_setup import EC_Setup


class EC_Data(EC_Setup):
    """ Reads and stores data from a TDMS file in the format of EC4 DAQ.

    When creating an opject the file path must be given.
     
    """
    def __init__(self, path = ""):
        super().__init__()
        self._area=1
        self._area_unit="cm^2"
        self.rotation =0
        self.rotation_unit ="/min"
        self.Time=np.array([],dtype=np.float64) 
        self.E=np.array([],dtype=np.float64)
        self.i=np.array([],dtype=np.float64)
        self.U=np.array([],dtype=np.float64)
        self.Z_E=np.array([],dtype=np.float64)
        self.Phase_E=np.array([],dtype=np.float64)
        self.Z_U=np.array([],dtype=np.float64)
        self.Phase_U=np.array([],dtype=np.float64)
        self.path=""
        #self.setup = {}
        """All setup information given in the file.
        """
        
        if path == "":
            #print("no path")
            return
        else:
            try:
                tdms_file = TdmsFile.read(path)
                tdms_file.close()
                self.path = str(path)
                self.Time = tdms_file['EC']['Time'].data
                self.i = tdms_file['EC']['i'].data
                self.E = tdms_file['EC']['E'].data
                self.name = tdms_file.properties['name']
                try:
                    self.Z_E = tdms_file['EC']['Z_E'].data #not all data file contains U channel
                    self.Phase_E = tdms_file['EC']['Phase_E'].data #not all data file contains U channel
                except KeyError:
                    pass
                try:
                    self.U = tdms_file['EC']['Ucell'].data #not all data file contains U channel
                except KeyError:
                    pass
                try:
                    self.Z_U = tdms_file['EC']['Z_cell'].data #not all data file contains U channel
                    self.Phase_U = tdms_file['EC']['Phase_cell'].data #not all data file contains U channel
                except KeyError:
                    pass
                try:
                    Items = tdms_file['Setup']['Item']
                    Value = tdms_file['Setup']['Value']
                    for x in range(len(Items)):
                        self.setup[Items[x]] = Value[x]
                except KeyError:
                    pass
                [self.area, self.setup_data._area_unit] = util.extract_value_unit(self.setup["Electrode.Area"])
                [self.rotation, self.setup_data.rotation_unit] = util.extract_value_unit(self.setup["Inst.Convection.Speed"])
                
            except FileNotFoundError :
                print(f"TDMS file was not found: {path}")
            except KeyError as e: 
                print(f"TDMS error: {e}") 
        
    
    def set_area(self,value,unit):
        self._area = value
        self._area_unit = unit

    def __str__(self):
        return f"{self.name}"


    def get_channel(self,datachannel:str):
        """
        Get the channel of the EC4 DAQ file.
        """
        match datachannel:
            case "Time":
                return self.Time,"t","s"
            case "E":
                return self.E, "E", "V"
            case "U":
                return self.U,"U", "V"
            case "i":
                return self.i,"i", "A"
            case "j":
                return self.i/self._area, "j", f"A/{self._area_unit}"
            case "Z_E":
                return self.Z_E,"Z_E", "Ohm"
            case "Z_U":
                return self.Z_U,"Z_U", "Ohm"
            case "Phase_E":
                return self.Phase_E,"Phase_E", "rad"
            case "Phase_U":
                return self.Phase_U,"Phase_U", "rad"
            case "R_E":
                #cosValue=self.Phase_E/self.Phase_E
                #index=0
                #for i in self.Phase_E:
                #    cosValue[index] = math.cos(self.Phase_E[index])
                #    index=index+1
                return self.Z_E * self.cosVal(self.Phase_E),"R_WE", "Ohm"
            case "E-IZ":
                return self.E - self.i*self.Z_E,"E-IZ", "V"
            
            case "E-IR":
                return self.E - self.i*self.Z_E,"E-IR", "V"
            case _:
                raise NameError("The channel name is not supported")
                #return np.array([2]), "No channel", "No channel"

    def cosVal(self,phase: float):
        cosValue=phase/phase
        max_index=len(phase)
        for i in range(max_index):
            cosValue[i] = math.cos(self.Phase_E[i])
        return cosValue



            
    
    def plot(self, x_channel:str, y_channel:str, **kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot = subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        '''
        xlable ="wrong channel name"
        xunit = "wrong channel name"
        ylable ="wrong channel name"
        yunit = "wrong channel name"
        
        options = plot_options(kwargs)
       
        try:
            xdata,xlable,xunit = self.get_channel(x_channel)
        except NameError as e:
            print(f"xchannel {x_channel} not supported") 
        finally:
            try:
                ydata,ylable,yunit = self.get_channel(y_channel)
            except NameError as e:
                print(f"ychannel {y_channel} not supported") 
        #except :
           
        #finally:
            '''add a the data to an existing plot or create a new'''
            try:
                ax = kwargs['plot']     
            except:
                fig = plt.figure()
                plt.suptitle(self.name)
                ax = fig.subplots()
            
            ydata = options.smooth_y(ydata)
            #try:
            #    y_smooth = options.get_y_smooth()
            #    if(y_smooth > 0):
            #        ydata = savgol_filter(ydata, y_smooth, 1)
            #except:
            #    pass
            xdata = options.smooth_x(xdata)
            
            #try:
            #    x_smooth = options.get_x_smooth()
            #    if(x_smooth > 0):
            #        xdata = savgol_filter(xdata, x_smooth, 1)
            #except:
            #    pass
            line =None
            try:
                line, = ax.plot(xdata,ydata)
                line.set_label(options.get_legend())
            except:
                pass
            ax.set_xlabel(f'{xlable} / {xunit}')
            ax.set_ylabel(f'{ylable} / {yunit}')
            return line, ax     

 