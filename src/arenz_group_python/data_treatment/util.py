"""
Utility module.

"""

import math
from scipy.signal import savgol_filter

def extract_value_unit(s:str):
    """_summary_

    Args:
        s (str): _description_

    Returns:
        value(float): the extracted value 
        unit(str): extract unit
    """
    unit =""
    value = math.nan
    try:
        list = s.strip().split(" ")
        value = float(list[0])
        unit = list[1]    
    finally:
        pass
    return value, unit



class plot_options:
    def __init__(self, kwargs):
        self.x_label="x"
        self.x_unit = "xunit"
        self.y_label = "y"
        self.y_unit = "y_unit"
        self.options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'plot' : 'newplot',
            'dir' : "all",
            'legend' : "noName",
            'xlabel' : "def",
            'ylabel' : "def"
        }
        self.options.update(kwargs)
        return
    
    def set_y_txt(self, label, unit):
        self.y_label = label
        self.y_unit = unit
        
    def set_x_txt(self, label, unit):
        self.x_label = label
        self.x_unit = unit
        
    def get_y_txt(self):
        return str(self.y_label + "("+ self.y_unit +")")
    def get_x_txt(self):
        return str(self.x_label + "("+ self.x_unit +")")
    
    def get_legend(self):
        return str(self.options['legend'])
    
    def get_x_smooth(self):
        return int(self.options['x_smooth'])
    
    def get_y_smooth(self):
        return int(self.options['y_smooth'])
    
    def get_dir(self):
        return str(self.options['dir'])
    
    def get_plot(self):
        return self.options['plot']
    
    def smooth_y(self, ydata):
        try:
            y_smooth = self.get_y_smooth()
            if(y_smooth > 0):
                ydata = savgol_filter(ydata, y_smooth, 1)
        except:
            pass
        return ydata
    
    def smooth_x(self, xdata):
        try:
            x_smooth = self.get_x_smooth()
            if(x_smooth > 0):
                xdata = savgol_filter(xdata, x_smooth, 1)
        except:
            pass
        return xdata
    
    