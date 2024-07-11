



class ec_setup_data:
        def __init__(self):
            self._setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
            self._area= 1.0
            self._area_unit="cm^2"
            self._rotation = 0.0
            self._rotation_unit ="/min"
            return

class EC_Setup:
    def __init__(self):
        #self._setup.setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
        #self._setup._area= 1.0
        #self._setup._area_unit="cm^2"
        #self._setup._rotation = 0.0
        #self._setup_rotation_unit ="/min"
        self.setup_data = ec_setup_data()
        return
    
    @property 
    def setup(self):
        """setup meta data

        Returns:
            dict[]: list of key words
        """
        return self.setup_data._setup
        
    @setup.setter
    def setup(self, value:float):
        self.setup_data._setup = value

    @property 
    def area(self):
        return self.setup_data._area
        
    @area.setter
    def area(self, value:float):
        self.setup_data._area = value

    @property
    def rotation(self):
        return self.setup_data._rotation

    @rotation.setter
    def rotation(self, value:float):
        return self.setup_data._rotation 

    def set_area(self,value:float,unit:str = ""):
        self.setup_data._area = value
        if unit == "":
            pass
        else:
            self.setup._area_unit = unit
        return
        
    def set_rotation(self,value:float,unit:str = ""):
        self.setup_data._rotation = value
        if unit == "":
            pass
        else:
            self.setup_data._rotation_unit = unit
        return
    




    