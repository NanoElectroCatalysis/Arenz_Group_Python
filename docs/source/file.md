



def save_key_values(file_path:Path, sample_name:str, properties:list, delimiter:str=DELIMITER):
    """Saves key values into a csv. The function add a row, or replace an existing row based on the 
    sample name. The first column will always sample name. The following columns will be the list values.

    Args:
        file_path (Path): Path to data file or relative path
        sample_name (str): Name of sample, will be the first column of the row.
        properties (list): List of values to be stored on the same row

    """