

from pathlib import Path
import inspect

class path_util:
    
    def _find_dir(self,path_to_caller: Path, dir_name:str):
        parents_dir = path_to_caller.parents
        path_to_dir = Path()
        for x in parents_dir:
            a = x / dir_name
            print(a.is_dir(),"\t\t",str(a) )
            if a.is_dir():
                path_to_dir = a
                break
        return path_to_dir      


    def raw_data_path(self, path_to_caller : Path ):
        """_summary_

        Args:
            path_to_caller (Path): _description_

        Returns:
            _type_: _description_
        """
        return self._find_dir(path_to_caller, "rawdata") 


    def callers(self):
        caller_fram = inspect.stack()[1]
        caller_filename_full = caller_fram.filename
        return caller_filename_full
        