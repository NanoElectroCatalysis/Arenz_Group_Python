# Docs:
# https://nanoelectrocatalysis.github.io/Arenz_Group_Python/


from .project.util_paths import Project_Paths, pDATA_RAW, pDATA_TREATED
from .file.file_dict import save_dict_to_file, load_dict_from_file, save_dict_to_tableFile
from .data_treatment import AutoClaveSynthesis
#from .data_treatment import EC_Data,EC_Datas,CV_Data,CV_Datas,AutoClaveSynthesis


#from .ec_data import * 

#__path__ = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_treatment')]

#print("loading arenz_group_python")
#print(__path__)

__version__= "0.3.6"

__all__ = ["Project_Paths","pDATA_RAW", "pDATA_TREATED",
            #"ec_data","EC_Data","EC_Datas","CV_Data","CV_Datas",
            "AutoClaveSynthesis", 
            "save_dict_to_file","load_dict_from_file", "save_dict_to_tableFile"
           ]



