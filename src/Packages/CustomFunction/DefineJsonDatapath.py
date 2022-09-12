from kivymd.app import MDApp
import os

def return_updated_data_path(basepath: str) -> str:
    ''' Given the database path, the year and month it return the path where the json file portfolio are stored'''

    # Define year folder path and check existance
    updated_data_path_year = basepath + 'Data/' + MDApp.get_running_app().VisualizedDate_year + '/' 
    check_folder_existance_with_compensation(updated_data_path_year)

    # Check if exists otherwise create the folder
    updata_data_path_month = updated_data_path_year + MDApp.get_running_app().VisualizedDate_month + '/'
    check_folder_existance_with_compensation(updata_data_path_month)

    # Check that the path actually exists
    return updata_data_path_month

def check_folder_existance_with_compensation(folder_path_to_check: str) -> None:
    ''' check the folder existance and if it does not exist, then create it'''

    if not (os.path.exists(folder_path_to_check)): os.mkdir(folder_path_to_check)