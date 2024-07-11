

class EC_Setup:
    def __init__(self):
        self.setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
        self._area= 1.0
        self._area_unit="cm^2"
        self._rotation = 0.0
        self._rotation_unit ="/min"
        return
    
    def set_area(self,value:float,unit:str = ""):
        self._area = value
        if unit == "":
            pass
        else:
            self._area_unit = unit
        return
        
    def set_rotation(self,value:float,unit:str = ""):
        self._rotation = value
        if unit == "":
            pass
        else:
            self._rotation_unit = unit
        return
    