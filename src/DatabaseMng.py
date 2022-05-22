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
    ### Root path ###
    database_path = 'Database/'

    ### Transaction path ###
    Inflow_path = 'InFlow_loc.json'
    Income_path = 'Earnings.json'
    Expences_path= 'Expences.json'
    TransactionIn_path = 'TransactionIn.json'
    TransactionOut_path = 'TransactionOut.json'
    ETF_ETC_path = 'ETF_ETC.json'
    Stocks_path = 'Stocks.json'
    Bonds_path = 'Bonds.json'
    Commodities_path = 'Commodities.json'
    Crypto_path = 'Crypto.json'
    Category_path = 'Category.json'

    ### Asset allocation resume ###
    CryptoAssets_path = 'CryptoAssets.json'

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

#########
# TESTS #
#########
TEST_TYPE = 1 # 0 for dictionary, 1 for list

if __name__ == '__main__':
    PathManager = PathManager_Class()
    if TEST_TYPE == 0:
        Manager = JsonManager_Class(PathManager.database_path, PathManager.Inflow_path)
        print(Manager.ReadJson())
        Manager.AddElement({'Unicredit1':[0,0]})
        Manager.RemoveElement('Unicredit2')
        print(Manager.ReadJson())
    elif TEST_TYPE == 1:
        Manager = JsonManagerList_Class(PathManager.database_path, PathManager.TransactionIn_path)
        print(Manager.ReadJson())
        Manager.ConcatenateElementList([0,0,0,0,0])
        print(Manager.ReadJson())
        Manager.RemoveElementFromList(3)
        Manager.SubstituteElementList(2,[1,1,1,1,1])
        print(Manager.ReadJson())
    


