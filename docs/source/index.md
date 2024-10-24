
# Install and Update
### Install: 
```python
 %pip install arenz_group_python
```
### Update
```python
 %pip install arenz_group_python -U
```


# Create a standard project with folders
```python
from arenz_group_python import Project_Paths as pp
pp().create_project_structure()
```

# Project Path constants
There are two path constants: pDATA_RAW, pDATA_TREATED
These constants return a PathLib to the raw data folder and the treated data folder.
```python
    from arenz_group_python import pDATA_RAW, pDATA_TREATED 
    file = pDATA_RAW / "FileName.txt"
    file2 = pDATA_TREATED / "FileName.txt"
```


<<<<<<< Updated upstream
# Save key values(dict) to a table-file(cvs)
```python
    from arenz_group_python import save_dict_to_tableFile
    # The target file is assumed to be in the treated data folder.
    Sample_Name = "sample 7"
    FileNameForKeyValues="keyValues.csv"
    KeyValues= [4,2,5,4,5]
    save_key_values(FileNameForKeyValues, Sample_Name, KeyValues) 
```
=======
# Save key values to a table

see example [ex_file_dict.md]
>>>>>>> Stashed changes

# Copy Raw data from the server into the raw data folder.

```python
    from arenz_group_python import Project_Paths
    pp = Project_Paths()
    project_name = 'projectname'
    user_initials = '' #This is optional, but it can speed up things
    path_to_server = 'X:/EXP_DB'
    pp.copyDirs(path_to_server, user_initials , project_name )
```
