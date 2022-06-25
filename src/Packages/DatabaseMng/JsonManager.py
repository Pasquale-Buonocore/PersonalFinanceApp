from Packages.CustomFunction.GetCryptoValue import GetCryptoValue
from Packages.DatabaseMng.PathManager import *
from os.path import exists
import json
import os


###################
# CUSTOM FUNCTION #
###################
path_manager = PathManager_Class()

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

    # Initialize the json file
    def Initialize_json(self):
        if not exists(self.database_path + self.json_path):
            self.SaveJsonFile({})

    # Save the json file
    def SaveJsonFile(self, dictionary):
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 4)

        # Writing to sample.json
        with open(self.database_path + self.json_path, "w") as outfile:
            outfile.write(json_object)

    # Read and return the dictionary
    def ReadJson(self):
        # Opening and Read JSON file
        with open(self.database_path + self.json_path, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        # Return dictionary
        return json_object

    # Add Element to the json file
    def AddElement(self, dictionary):
        # Read json
        json_object = self.ReadJson()
            
        # Add items in dictionary if not already present
        for key in dictionary.keys():
            # if key not in json_object.keys():
            json_object.update({key : dictionary[key]})
        
        # Save new json file
        self.SaveJsonFile(json_object)

    # Substitute Element to the json file
    def SubstituteElement(self, Old_element, New_Item):
        new_dict = {}

        # Read json and iterate over it
        json_object = self.ReadJson()
        
        for key in json_object:
            if key in Old_element.keys():
                new_dict.update(New_Item)
            else:
                new_dict.update({key:json_object[key]})
        
        # Save new json file
        self.SaveJsonFile(new_dict)

    # Remove Element to the json file
    def RemoveElement(self, Element):
        # Read json
        json_object = self.ReadJson()

        # Remove Item
        if Element in json_object.keys():
            json_object.pop(Element)

        # Save new Json file
        self.SaveJsonFile(json_object)