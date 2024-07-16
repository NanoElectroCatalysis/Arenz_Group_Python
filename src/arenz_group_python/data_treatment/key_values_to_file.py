
import csv
from pathlib import Path
from .util_paths import Project_Paths


DELIMETER = '\t'

def save_key_values(file_path:Path, sample_name:str, properties:list):

    all_data =[]
    new_row = [sample_name] + properties
    sample_already_in_dataset= False
    if file_path == "":
        print( "empty path ")
        return False
    elif file_path.exists:    
        with open(file_path, 'r', newline='') as csvfile:
            #reads the file
            spamreader = csv.reader(csvfile, delimiter=DELIMETER, quotechar='|')

            all_data =[]
            i=0
            sample_already_in_dataset = False
            for row in spamreader:
                all_data.append(row)
                if(row[0] == sample_name):
                    print("sample name found -  updating row")
                    all_data[i] = new_row
                    sample_already_in_dataset= True
                i+=1
            if not sample_already_in_dataset:
                print("sample not found -  adding row")
                all_data.append(new_row)
                
    else:
        print("new file.")
        all_data.append(new_row)

    #print(all_data) 
    with open(file_path, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=DELIMETER,
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in all_data:
            spamwriter.writerow(row) #row
    
    return True
                