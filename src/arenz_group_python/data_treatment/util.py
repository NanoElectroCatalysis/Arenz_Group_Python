"""
Utility module.

"""

import math
from scipy.signal import savgol_filter, medfilt
from scipy import ndimage, datasets
import matplotlib.pyplot as plt
from fractions import Fraction


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

#######################################################################################

class symbol_string:
    def __init__(self,s:str=""):
        self.symbols = s

    def __str__(self) -> str:
        return self.symbols
    
    def __add__(self, other):
        s = quantity_fix(self.symbols + other.symbols)             
        return symbol_string(s)
    
    def __pow__(self, other):
        s = quantity_fix(self.symbols,other)    
        return symbol_string(s)

class Quanity_Value_Unit:
    def __init__(self, value: float | str =0.0 , unit="", quantity=""):
        if isinstance(value, str):
            self.value,self.unit = extract_value_unit(value)
            self.quantity = ""
        else:
            self.value = value
            self.unit = unit
            self.quantity =quantity

        
    def __str__(self) -> str:
        return f'{self.value:.3e} {self.unit}'
    
    def __float__(self) -> float:
        return self.value
    
    def __add__(self, other):
        if self.unit == other.unit:
            v = Quanity_Value_Unit()
            v.value= self.value + other.value             
        return Quanity_Value_Unit(self.value+other.value,self.unit, self.quantity)
    
    def __mul__(self, other):
        v = Quanity_Value_Unit()
        if isinstance(other, Quanity_Value_Unit):
            v.value = self.value * other.value
            v.unit = quantity_fix(self.unit +" "+ other.unit)
            v.quantity = quantity_fix(self.quantity + " " + other.quantity)
        else:
            v.value = self.value * other
            v.unit = self.unit
            v.quantity = self.quantity
        return v
    
    def __div__(self, other):
        v = Quanity_Value_Unit()
        if isinstance(other, Quanity_Value_Unit):
            v.value = self.value / other.value
            v.unit = quantity_fix(self.unit + quantity_fix(other.unit,-1))
            v.quantity = quantity_fix(self.quantity + quantity_fix(other.quantity,-1))
        else:
            v.value = self.value / other
            v.unit = self.unit
            v.quantity = self.quantity      
        return v
    
    def __truediv__(self, other):
        v = Quanity_Value_Unit()
        if isinstance(other, Quanity_Value_Unit):
            v.value = self.value / other.value
            v.unit = quantity_fix(self.unit +quantity_fix(other.unit,-1))
            v.quantity = quantity_fix(self.quantity +  quantity_fix(other.quantity,-1))
        else:
            v.value = self.value / other
            v.unit = self.unit
            v.quantity = self.quantity  
        return v
    
    def __pow__(self, other):
        v = Quanity_Value_Unit()
        v.value = self.value ** other
        v.unit = quantity_fix(self.unit,other)    
        v.quantity = quantity_fix(self.quantity,other) 
        return v

def get_unit_and_exponent(s:str):
    aa = s.split("^",2)
    nyckel = aa[0]
    sign = 1
    fac =  1.0
    if nyckel.startswith("/"):
        nyckel = nyckel[1:]
        sign = -1
    if len(aa)>1:                   #if "^" was found.
        fac = float(aa[1]) 
    return nyckel, sign*fac

    
def quantity_fix(s:str, factor:float = 1):
    list_of_quantities = s.split(" ", 100)
    k={}
    for single_quantity in list_of_quantities:
        nyckel, exponent = get_unit_and_exponent(single_quantity)
        val = float(k.get(nyckel, 0))  
        k[nyckel] = val + exponent
    prep={} 
    for key, value in k.items():
        if int(value*100) != 0:
            prep[key] = value * factor
    sr =""
    #print ("quantity_fix:",prep)  
    for key, value in prep.items():
        if int(value*10) == 10:
            sr = sr +" " + key
        elif int(value) == value:
            sr = sr+ f' {key}^{value:.0f}'
        else:
            sr = sr+ f' {key}^{value:.1f}'
    return sr.strip()

###################################
