# Leave it empty. This is just a special file that tells pip that your main module is in this folder. 
# No need to add anything here. Feel free to delete this line when you make your own package.

#from anyt import EC_Data
"""_summary_
Module for reading binary TDMS files produced by EC4 View\n

ec_data is used to load in the raw files. 

"""
import os
#__path__ = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contents')]
__all__ = ["EC_Data", "ec_data","CV_Data","CV_Datas"]


from .ec_data import EC_Data 
from .cv_data import CV_Data
from .cv_datas import CV_Datas 
from .util import * 


#Import the submodules
#from . import ec_data