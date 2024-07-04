""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import matplotlib.pyplot as plt

class EC_Data:
    """ Reads and stores data from a TDMS file in the format of EC4 DAQ.

    When creating an opject the file path must be given.
     
    """
    def __init__(self, path):
        self._area=1
        self._area_unit="cm^2"
        self.Time=[]
        self.E=[]
        self.i=[]
        self.U=[]
        self.Z_E=[]
        self.Phase_E=[]
        self.Z_U=[]
        self.Phase_U=[]
        self.path=""
        
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

    def cosVal(self,phase):
        cosValue=phase/phase
        max_index=len(phase)
        for i in range(max_index):
            cosValue[i] = math.cos(self.Phase_E[i])
        return cosValue

    
    def plot(self, x_channel:str,y_channel:str,**kwargs):
        '''
        plots y_channel vs x_channel.
        to add to a existing plot, add the argument: 
        "ax=subplot"
        
        '''
        xlable ="wrong channel name"
        xunit = "wrong channel name"
        ylable ="wrong channel name"
        yunit = "wrong channel name"
        
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
            try:
                ax = kwargs['ax']     
            except:
                fig = plt.figure()
                plt.suptitle(self.name)
                ax = fig.subplots()

            try:
                ax.plot(xdata,ydata)
            except:
                pass
            ax.set_xlabel(f'{xlable} / {xunit}')
            ax.set_ylabel(f'{ylable} / {yunit}')
            return ax     

 