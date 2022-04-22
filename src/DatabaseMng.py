from os.path import exists
import json
"""
This file aims to initialize the json file in the database folder [If it does not exist already]
# The database will be contains the following files:

- The IN FLOW location: 
    Infos: Name, Last month value, Actual Value (It will be computed)
- The OUT FLOW location
"""
#############
# CONSTANST #
#############
class PathManager_Class():
    database_path = 'Database/'
    Inflow_path = 'InFlow_loc.json'

###################
# CUSTOM FUNCTION #
###################



###########################
# Initialize json manager #
###########################
class JsonManager_Class():
    def __init__(self, database_path, json_file):
        self.database_path = database_path
        self.json_path = json_file
        self.Initialize_json()

    #################
    # CLASS METHODS #
    #################

    # Initialize the InFlow location json file
    def Initialize_json(self):
        if not exists(self.database_path + self.json_path):
            self.SaveJsonFile(self.database_path + self.json_path, {})

    # Save the json file
    def SaveJsonFile(self, dictionary):
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 4)

        # Writing to sample.json
        with open(self.database_path + self.json_path, "w") as outfile:
            outfile.write(json_object)

    # Add Element to the InFlow location json file
    def AddElement(self, dictionary):
        # Read json
        json_object = self.ReadJson()
            
        # Add items in dictionary if not already present
        for key in dictionary.keys():
            if key not in json_object.keys():
                json_object.update({key : dictionary[key]})
        
        # Save new json file
        self.SaveJsonFile(json_object)
    
    # Remove Element to the InFlow location json file
    def RemoveElement(self, Element):
        # Read json
        json_object = self.ReadJson()

        # Remove Item
        if Element in json_object.keys():
            json_object.pop(Element)

        # Save new Json file
        self.SaveJsonFile(json_object)
    
    # Read and return the dictionary
    def ReadJson(self):
        # Opening and Read JSON file
        with open(self.database_path + self.json_path, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        # Return dictionary
        return json_object

#########
# TESTS #
#########
if __name__ == '__main__':
    PathManager = PathManager_Class()
    InFlow_obj = JsonManager_Class(PathManager.database_path, PathManager.Inflow_path)
    print(InFlow_obj.ReadJson())
    InFlow_obj.AddElement({'Unicredit1':[0,0]})
    InFlow_obj.RemoveElement('Unicredit2')
    print(InFlow_obj.ReadJson())

    


