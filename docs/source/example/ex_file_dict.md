---
title: Save and load key values(dict)
parent: Examples
---
# Save and load key values(dict)

## Save and load key values(dict) from a single sample into a file. 

´´´python 
from arenz_group_python import save_dict_to_file,load_dict_from_file
´´´

´´´python 
file_path= "My_Dict_File.txt"
keyValues= {
    "firstKey" : 5.23,
    "secondKey": "A string" 
}
keyValues["thridKey"] = 32.543
print(keyValues)
save_dict_to_file(file_path,keyValues)
Loaded_KeyValues = load_dict_from_file(file_path)
print(Loaded_KeyValues)
´´´
## Save and load key values(dicts) from a multiple samples into a file. 

```python 
from arenz_group_python import save_dict_to_tableFile,open_dict_from_tablefile
```
The "save_dict_to_tableFile" will save the dict as a row in the table. First column is the sample name.
```python

table_file_path= "My_TableF_File.txt"
sample1_name = "MySample_1"
sample1_keyValues= {
    "firstKey" : 5.23,
    "secondKey": "A string" 
    "thridKey": 2132 
}
Add a second sample.
save_dict_to_tableFile(table_file_path, sample1_name, sample1_keyValues )
```
```python
sample2_name = "MySample_2"
sample2_keyValues= {
    "firstKey" : 324325.23,
    "secondKey": "B string" 
    "thridKey": 24324232 
}
save_dict_to_tableFile(table_file_path, sample2_name, sample2_keyValues )

```
If the same sample name is already in the file, the data will updated.
```python
sample2_name = "MySample_2"
sample2_keyValues= {
    "firstKey" : 123.23,
    "secondKey": "c string" 
    "thridKey": 123 
}
save_dict_to_tableFile(table_file_path, sample2_name, sample2_keyValues )

```

Open the tablefile as a numpy dataFrame.
```python
df = open_dict_from_tablefile()

```
