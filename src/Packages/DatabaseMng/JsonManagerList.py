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
class JsonManagerList_Class():
    def __init__(self, database_path, json_file):
        self.database_path = database_path
        self.json_path = json_file
        self.Initialize_json()
        # If it is not empty:
        # 1. Check if the indexes are correctly ordered
        # 2. Save a new version of the json file if it has been previously corrupted
        self.SaveJsonFile(self.ReadJson())

    #################
    # CLASS METHODS #
    #################
    def OrderList(self, json_object):
        # Initialize variables
        OutDict = {}
        counter = 1

        # Reorganize json
        for key in json_object.keys():
            OutDict.update({counter: json_object[key]})
            counter = counter + 1

        # Update counter
        self.ElementCounter = counter -1 

        return OutDict

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
        return self.OrderList(json_object)

    # Initialize the internal counter as the number of item in the list
    def InitializeCounter(self):
        # Read json
        json_object = self.ReadJson()
        # Update the counter
        return len(json_object)
    
    # Concatenate Element to the json file
    def ConcatenateElementList(self, ElementList):
        # Read json
        json_object = self.ReadJson()

        # Add Item independetly of the type
        self.ElementCounter = self.ElementCounter + 1
        json_object.update({self.ElementCounter : ElementList})

        # Save new json file
        self.SaveJsonFile(json_object)

    # Substitute the element in a list
    def SubstituteElementList(self, ItemNum, NewList):
        # Read json
        json_object = self.ReadJson()

        if ItemNum in json_object.keys():
            json_object[ItemNum] = NewList
        
        # Save Json
        self.SaveJsonFile(json_object)

    # Remove Element from the list
    def RemoveElementFromList(self, ItemNum):
        # Read json
        json_object = self.ReadJson()

        if ItemNum in json_object.keys():
            json_object.pop(ItemNum)
        
        # Save Json
        self.SaveJsonFile(self.OrderList(json_object))