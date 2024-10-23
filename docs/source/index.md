Python


# Install 
>   !pip install arenz_group_python

# Create a standard project with folders

> from arenz_group_python import Project_Paths
> pp= Project_Paths().create_project_structure(nb_path)

# Project Path constants:
There are two path constants: pDATA_RAW, pDATA_TREATED
These constants return a PathLib to the raw data folder and the treated data folder.

> import arenz_group_python import 
> file = pDATA_RAW / "FileName"
> file2 = pDATA_TREATED / "FileName"

