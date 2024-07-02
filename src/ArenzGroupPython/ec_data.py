from nptdms import TdmsFile



class EC_Data:
    def __init__(self, path):
        tdms_file = TdmsFile.read(path)
        tdms_file_groups = tdms_file.groups()
        self.path = str(path)
        self.Time = tdms_file_groups[0]['Time'].data
        self.i = tdms_file_groups['EC']['i'].data
        self.E = tdms_file_groups['EC']['E'].data
        self.name = tdms_file.properties['name']

        tdms_file.close()
    
    def __str__(self):
        return f"{self.path}"


#p1 = Person("John", 36)

#print(p1.name)
#print(p1.age)

###
#data in the folder, e.g.
#tdms_file = TdmsFile.read("data/Steps_102346.tdms")
#tdms_file_groups = tdms_file.groups()
#tdms_file_df = tdms_file.as_dataframe()

# grab the columns in the file
#tdms_file_groupEC_i_file0s50mV = tdms_file_groups[0]['i']
#tdms_file_groupEC_t_file0s50mV = tdms_file_groups[0]['Time']
#tdms_file_groupEC_E_file0s50mV = tdms_file_groups[0]['E']
#tdms_file_groupEC_R_file0s50mV = tdms_file_groups[0]['Z_E']

# rename and create a numpy-array with the data
#current_file0s50mV = tdms_file_groupEC_i_file0s50mV.data
#time_file0s50mV = tdms_file_groupEC_t_file0s50mV.data
#potential_file0s50mV = tdms_file_groupEC_E_file0s50mV.data
#resistivity_file0s50mV = tdms_file_groupEC_R_file0s50mV.data
