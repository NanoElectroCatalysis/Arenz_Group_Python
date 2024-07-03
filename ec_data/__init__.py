# Leave it empty. This is just a special file that tells pip that your main module is in this folder. 
# No need to add anything here. Feel free to delete this line when you make your own package.

#from anyt import EC_Data

import os

from .ec_data import * 

__path__ = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contents')]