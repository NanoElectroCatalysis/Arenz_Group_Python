from elabapi_python.rest import ApiException

#import elabftw.elabftw
from .elabftw import API_KEY_NAME

from .elabftw import download_experiment_single,api_read_experiments
from arenz_group_python import Project_Paths



def connect(verify_ssl: bool = True):
    """Connect to the database.

    Args:
        verify_ssl (bool, optional): _description_. Defaults to True.
    """
    from .elabftw import connect_to_database
    connect_to_database(verify_ssl)
   
    

def download_experiment(ID_value:str|int, create_Tree = True):
    """Download all experimental information and saves it into data_raw folder.

    Args:
        ID_value (str, optional): experiment ID number as an interger, or as a string: ex. "ATS-JF060".
        create_Tree (bool, optional): download all associated experiments too. Defaults to True.
    """
    ID = None
    if isinstance(ID_value,int):
        ID = ID_value 
    else:       
        ID = get_experiment_ID(ID_value)
     
    if create_Tree:
        download_experiment_tree(ID)
    else:
        download_experiment_single(ID, Project_Paths().rawdata_path)
        return
        

    
def download_experiment_tree(ID):
    """
    Get the experiment with the given ID from the eLabFTW database and save it to the rawdata folder.
    
    Parameters
    ----------
    ID : str
        The ID of the experiment to retrieve.
    
    Returns
    -------
    None
    """
    from .elabftw import create_structure_and_download_experiments
    try:
        create_structure_and_download_experiments(ID)
    except ApiException as e:
        if e.status == 404:
            print(f"Experiment with ID {ID} not found. error 404")
        elif( e.status == 401):
            print(f"The API key is not correct. Check your .env file for '{API_KEY_NAME}'-key . error 401")
        else:
            print(f"An error occurred: {e}")
            
def get_experiment(ID_value,**kwargs):
    """Get experiment ID

    Args:
        ID_value (str | int): experiment identifier

    Returns:
        tuplet: experiment
    """
    if isinstance(ID_value,int):
        ID = ID_value
    else:
        ID = get_experiment_ID(ID_value)
    from .elabftw import api_get_experiment
    return api_get_experiment(ID,**kwargs)

def get_experiment_ID(ID_name):
    """Get experiment ID

    Args:
        ID_name (str): experiment identifier

    Returns:
        int: experiment id number
    """
    list_result = api_read_experiments(q=ID_name)
    if list_result:
        for item in list_result:
            title = str(item.title).split()
            if title[0].casefold() == str(ID_name).casefold():
                return int(item.id)
    return None