

from pathlib import Path
import inspect
from enum import StrEnum

class PROJECT_FOLDERS(StrEnum):
    rawdata = "data_raw"
    treated_data = "data_treated"
    scripts = "py_scripts"
    nb_models = "notebooks_models"
    nb_exploration = "notebooks_exploration_cleaning" 

############################################################
############################################################
class Project_Paths:
    """
    Class Project_Paths can be used to more easily create the paths typically used in a project

        - "Project_Paths().cwd" to go get current working directory

        - "Project_Paths().data_rawdata" to go get rawdata directory

        - "Project_Paths().data_path" to go get current working directory

        - "Project_Paths().data_path" to go get current working directory


        create_project_structure( Path) to create a project folder tree. Note, it uses the executing notebook as root dir if no path is given
    
    """
    #######################################################################
    def _find_dir(self,path_to_caller: Path, dir_name:str) -> Path:
        
        path_to_dir = Path()
        if isinstance(path_to_caller, Path):  #make sure the path is a Path
            p = path_to_caller
        else:
            p = Path(path_to_caller)

        if (p / dir_name).exists():
             path_to_dir = p / dir_name   
        else:   
            parents_dir = p.parents
            
            for x in parents_dir:
                a = x / dir_name
                #print(a.is_dir(),"\t\t",str(a) )
                if a.is_dir():
                    path_to_dir = a
                    break
        if path_to_dir == Path():
            raise NotADirectoryError(f'\"{dir_name}\" could not be found as a branch of the folder tree form the notebook.\nPlease use standard project structure.')
        return path_to_dir      

    ######################################################################################
    def _rawdata_path(self, path_to_caller : Path = Path.cwd() ) -> Path:
        """_summary_

        Args:
            path_to_caller (Path): _description_

        Returns:
            Path: Path to rawdata folder
        """
        p = path_to_caller
        k = Path()
        #print(PROJECT_FOLDERS.rawdata)
        if path_to_caller == Path(""):
            p = Path.cwd()
        try:
            k = self._find_dir(p, str(PROJECT_FOLDERS.rawdata))
        except NotADirectoryError as err:
            print(err)
        
        return k 
        #return Path(".") 
    
    ###############################################################################################
    def _treated_data_path(self, path_to_caller : Path = Path.cwd() ) -> Path:
        """_summary_

        Args:
            path_to_caller (Path): _description_

        Returns:
            Path: path to "treated_data" folder
        """
        try:
            k = self._find_dir(path_to_caller, str(PROJECT_FOLDERS.treated_data))
        except NotADirectoryError as err:
            print(err)
        
        return k 

    #################################################################################################
    def callers(self) -> str:
        caller_fram = inspect.stack()[1]
        caller_filename_full = caller_fram.filename
        return caller_filename_full

    #####################################################################
    def _current_working_dir(self)  -> Path:
        return Path.cwd()
    
    #####################################################################################################
    @property 
    def cwd(self)  -> Path:
        return self._current_working_dir() 
        
    ####################################################################################################
    @property 
    def rawdata_path(self)  -> Path:
        """return to raw data path"""
        return self._rawdata_path()
    
    ##################################################################################################
    @property 
    def data_path(self)  -> Path:
        """return to data path"""
        return self._treated_data_path()
    
    ##################################################################################################
    def create_project_structure(self, project_path: Path):
        """The fx creates a standard folder structure for projects.

        Args:
            project_path (Path): Path to the base folder of the project. 
        """
        for folderPath in PROJECT_FOLDERS:
            try:
                newFolder =  project_path / folderPath
                newFolder.mkdir()
            except FileExistsError as err:
                print(f"-\"{folderPath}\" exists already as a folder")
            except FileNotFoundError as err:
                print("The path to the project is not correct")
                return
        
        make_project_files( project_path)
        make_project_files_data(project_path)           
        
#end of clasee ############################################################################   
                    
################################################################################
def make_project_files( main_dir: Path):               
    print("\ncreating files:\n")
    def_files = [
        PROJECT_FOLDERS.nb_models + "/modelData.ipynb",
        PROJECT_FOLDERS.scripts +"/my_Module.py"
    ]
    for file in def_files:
        try:
            fo= open(file,"x")
            fo.close()
            print(f"+\"{file}\" was created")
        except FileExistsError:
            print(f"-\"{file}\" already exists")

    path = main_dir / PROJECT_FOLDERS.scripts / "__init__.py"
    try:
        with open(path,"x") as f:
            f.write("# Leave it empty. This is just a special file that tells pip that your main module is in this folder.\n# No need to add anything here. Feel free to delete this line when you make your own package.")
            f.close()
        print(f"+\"{path.name}\" was created")
    except FileExistsError :
        print(f"-\"{path.name}\" already exists")

    
    path = main_dir / PROJECT_FOLDERS.nb_exploration / "extractData.ipynb"
    try:
        with open(path,"x") as f:
            f.write('''{
    "cells": [
    {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Exploring the data",
        "use this notebook and others to extract data.",
        "",
        "To use with electrochemistry data, use the following import:",
        "from arenz_group_python import EC_Data #to load in a single tdms file",
        "",
        "from arenz_group_python import CV_Data # to import a single CV.",
        "",
        "from arenz_group_python import CV_Datas # to import a multiple CVs at once form a list of paths",
        "",
        "from arenz_group_python import Project_Paths # to load in path constants.",
        "",
        "from arenz_group_python import save_key_values # to save key values.",
        ""
        ]
    },
    {
    "cell_type": "code",
    "execution_count": null,
    "metadata": {},
    "outputs": [],
    "source": [
        "#from arenz_group_python import EC_Data",
        "#from arenz_group_python import Project_Paths",
        "#from arenz_group_python import CV_Data",
        "",
        "#if there is a file in the rawdata folder:",
        "#PATH_TO_FILE = Project_Paths().rawdata_path / \'FILE_NAME\' ",
        "#file1 = EC_Data(\'PATH_TO_FILE\')",
        "#file1.plot(\'E\',\'i\') # for a i vs E plot "
    ]
    },
    {
    "cell_type": "code",
    "execution_count": null,
    "metadata": {},
    "outputs": [],
    "source": [
        "from arenz_group_python import save_key_values",
        "",
        "# The target file is assumed to be in the data folder",
        "save_key_values(\'extracted_values.csv\',\'sample 7\', [4,2,5,4,5]) "
    ]
    }
    ],
    "metadata": {
    "kernelspec": {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
    },
    "language_info": {
    "name": "python",
    "version": "3.11.5"
    }
    },
    "nbformat": 4,
    "nbformat_minor": 2
    }''')
            f.close()
        print(f"+\"{path.name}\" was created")
    except FileExistsError:
        print(f"-\"{path.name}\" already exists")   

################################################################################                
def make_project_files_data( main_dir: Path):               
 

    path = main_dir / PROJECT_FOLDERS.rawdata / "README.txt"
    try:
        with open(path,"x") as f:
            f.write("# Use the rawdata folder to store all experimental data. ONLY!!!!.")
            f.close()
        print(f"+\"{path.name}\" was created")
    except FileExistsError :
        print(f"-\"{path.name}\" already exists")
        
        
    ##### PATH to data file    
    path = main_dir / PROJECT_FOLDERS.treated_data / "README.txt"
    try:
        with open(path,"x") as f:
            f.write("# Use the data folder to store all extracted values from data manipulation. NO RAW DATA!!!!.")
            f.close()
        print(f"+\"{path.name}\" was created")
    except FileExistsError :
        print(f"-\"{path.name}\" already exists")
        
    path = main_dir / PROJECT_FOLDERS.treated_data / "extracted_values.csv"
    try:
        with open(path,"x") as f:
            f.write("")
            f.close()
        print(f"+\"{path.name}\" was created")
    except FileExistsError :
        print(f"-\"{path.name}\" already exists")
    ###########################################################################################

def find_project_files_data2( server_dir: Path, fileID:str="*.*"):
    pp = Project_Paths()
    rawdata_path = pp.rawdata_path
    if server_dir.is_dir:
        print("dir ok")
        for child in server_dir.iterdir(): child 

