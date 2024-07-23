



class ec_setup_data:
        def __init__(self):
            self._setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
            self._area= 1.0
            self._area_unit="cm^2"
            self._rotation = 0.0
            self._rotation_unit ="/min"
            self.name =""
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
    def area_unit(self):
        return self.setup_data._area_unit
        
    @area_unit.setter
    def area(self, value:str):
        self.setup_data._area_unit = value


    @property
    def rotation(self):
        return self.setup_data._rotation

    @rotation.setter
    def rotation(self, value:float):
        """set the rotation rate

        Args:
            value (float): rotation rate
        """
        self.setup_data._rotation = value

    @property
    def rotation_unit(self):
        return self.setup_data._rotation_unit

    @rotation_unit.setter
    def rotation_unit(self, value:str):
        """set the rotation rate

        Args:
            value (str): rotation unit
        """
        self.setup_data._rotation_unit = value


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
    
    def legend(self, **kwargs)-> str:
        """_summary_

        use: legend = '?' to get a list of possible options
        Returns:
            str: legend 
        """
        s = str()
        #print(kwargs)
        if 'legend' in kwargs:
            item = kwargs['legend']
            if item == '?':
                #print(self.setup_data._setup)
                return "_"
            elif item == "name":
                return self.setup_data.name
            elif item in self.setup_data._setup:
                #print("items was found", item)
                s = self.setup_data._setup[item]
                return s
            else:
                return item
        return "_"
        





    