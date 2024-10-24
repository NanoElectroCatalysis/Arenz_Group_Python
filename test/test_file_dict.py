

from arenz_group_python import save_dict_to_file,load_dict_from_file,save_dict_to_tableFile,open_dict_from_tablefile
from pathlib import Path 
#"import inc_dec    # "The code to test
import unittest   # The test framework

cwd = Path().cwd()
temp_dir = cwd /"TEMP_Project"

keyValues_1= {
            "firstKey" : 5.23,
            "secondKey": "A string" ,
            "thridKey" :33
        }
        
keyValues_2= {
    "firstKey" : 511.23,
    "secondKey": "B string",
    "thridKey" :21 
        }

class test_file_dict(unittest.TestCase):
    
    def test_SaveLoad_File(self):
        
        pa= Path().cwd() / "TEMP_Project"
        print(pa, pa.exists())

        try:
            pa.mkdir()
        except:
            pass
        
        file_path= pa / "My_Dict_File.txt"

        

        save_dict_to_file(file_path,keyValues_1)
        self.assertTrue(file_path.exists)
        keyValues_B = load_dict_from_file(file_path)
        self.assertDictEqual(keyValues_1, keyValues_B)  
        
    def test_SaveLoad_TB(self):
        
        pa= Path().cwd() / "TEMP_Project"
        print(pa, pa.exists())

        try:
            pa.mkdir()
        except:
            pass
        
        TB_file_path= pa / "My_TB_File.txt"
        save_dict_to_tableFile(TB_file_path,"sample_name1", keyValues_1)
        self.assertTrue(TB_file_path.exists)
        save_dict_to_tableFile(TB_file_path,"sample_name2", keyValues_2)
        df = open_dict_from_tablefile(TB_file_path)
        
        list_names = ["sample_name1","sample_name2"]
        list_names_loaded = list(df.get("name"))
        self.assertListEqual(list_names,list_names_loaded)
        subdf = df.to_dict()
        
        
            

        
     
        
        
if __name__ == '__main__':
    unittest.main()
