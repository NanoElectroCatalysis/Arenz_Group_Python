# Arenz_Group_Python
Python libs for Arenz Group

## Documentation

https://nanoelectrocatalysis.github.io/Arenz_Group_Python/

# Get started
In the project root folder, create a jupyter file.

## Package installation or upgrade using Jupyter

In order to install this package use the following line in a jupyter notebook: 
'''python
%pip install arenz_group_python
'''
In order to upgrade this package use the following line in a jupyter notebook: 

'''python
%pip install arenz_group_python -U
'''

Restart the kernal.

## Create the basic project folder structure.

'''python
from arenz_group_python import create_project_structure
create_project_structure()
'''

## Import raw data files.
Make sure that all the folders you want to import as a file called:
<IDENTIFYIER>.tag 
where <IDENTIFYIER> can be a project name, example: "project.tag"
'''python
from arenz_group_python import Project_Paths
pp = Project_Paths()
project_name = 'projectname'
user_initials = '' #This is optional, but it can speed up things
path_to_server = 'X:/EXP_DB'
pp.copyDirs(path_to_server, user_initials , project_name )
'''

## Load values from file
'''python
from arenz_group_python import load_dict_from_file
load_dict_from_file

'''

## Save values in a dict to table file(cvs)
'''
from arenz_group_python import save_dict_to_tableFile

save_dict_to_tableFile(file_path, sample_name, properties)
'''