from os.path import exists
import json
"""
This file aims to initialize the json file in the database folder [If it does not exist already]
# The database will be contains the following files:

- The IN FLOW location: 
    Infos: Name, Last month value, Actual Value (It will be computed)
- The OUT FLOW location
"""
import os
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

class PortfoliosManager_Class():
    """ The json contains several Portfolios, which are organized as:

    Portfolio1
        - Assets
            - Asset1
                - Transactions
                - Asset1 Statistics

            - Asset2
                - Transactions
                - Asset2 Statistics

            - Asset3
                - Transactions
                - Asset3 Statistics

        - Statistics (which will be used to fill the dashboard at each page opening)

    There might be more than one portfolio
    """

    def __init__(self, database_path, json_file):
        self.database_path = database_path
        self.json_path = json_file
        self.Initialize_json()

    #################
    # CLASS METHODS #
    #################

    # Initialize the json file - TESTED
    def Initialize_json(self):
        if not exists(self.database_path + self.json_path):
            self.SaveJsonFile({})

    # Save the json file - TESTED
    def SaveJsonFile(self, dictionary):
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 6)

        # Writing to sample.json
        with open(self.database_path + self.json_path, "w") as outfile:
            outfile.write(json_object)

    # Read and return the dictionary - TESTED
    def ReadJson(self):
        # Opening and Read JSON file
        with open(self.database_path + self.json_path, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        # Return dictionary
        return json_object

    ########################
    # PORTFOLIO MANAGEMENT #
    ########################

    # Add Element to the json file - TESTED
    def AddPortfolio(self, NewPortfolioDict):
        # Read json
        json_object = self.ReadJson()
            
        # Add items in dictionary if not already present
        for key in NewPortfolioDict.keys():
            if key not in json_object.keys():
                json_object.update({key : NewPortfolioDict[key]})
            else:
                # Open Popup Warning that the element already exist
                print('Portfolio ' + key + ' already present in DB. Not added.')

        # Save new json file
        self.SaveJsonFile(json_object)

    # Substitute Element to the json file - TESTED
    def ModifyPortfolio(self, OldPortfolioName, NewPortfolioName, NewPortfolioCurrency):
        # Define a new dict containg the new Json
        new_dict = {}

        # Read json and iterate over it
        json_object = self.ReadJson()
        
        # Modify portfolio name and currency
        OldPortfolio = json_object[OldPortfolioName]
        OldPortfolio['Statistics']['Currency'] = NewPortfolioCurrency

        # New dictionary in input
        for PortfoliosKey in json_object.keys():
            if PortfoliosKey == OldPortfolioName:
                new_dict.update({NewPortfolioName : OldPortfolio})
            else:
                new_dict.update({PortfoliosKey:json_object[PortfoliosKey]})
        
        # Save new json file
        self.SaveJsonFile(new_dict)

    # Remove Element to the json file -TESTED
    def RemovePortfolio(self, PortfolioName):
        # Read json
        json_object = self.ReadJson()

        # Remove Item
        if PortfolioName in json_object.keys():
            json_object.pop(PortfolioName)

        # Save new Json file
        self.SaveJsonFile(json_object)
    
    # Initialize a new portfolio structure - TESTED
    def InitializeNewPortfolio(self, PortfolioName, PortfolioInitList = ['$', 1000, 8, 230]): 
        # A new portfolio will contains two dictionary 1) Assets and Statistics
        Asset = {'Assets': {}}

        StatisticDict = {'Currency': str(PortfolioInitList[0])}
        StatisticDict.update({'TotalValue' : int(PortfolioInitList[1])})
        StatisticDict.update({'NumberOfAssets' : int(PortfolioInitList[2])})
        StatisticDict.update({'TotalProfit' : int(PortfolioInitList[3])})
        Statistic = {'Statistics' : StatisticDict }

        # Initialize dictionary with the portfolio
        NewPortfolioDict = {PortfolioName : {}}
        NewPortfolioDict[PortfolioName].update(Asset)
        NewPortfolioDict[PortfolioName].update(Statistic)
        return NewPortfolioDict

    # Read Portfolio - TESTED 
    def ReadPortfolio(self, PortfolioName):
        # Read json and iterate over it
        json_object = self.ReadJson()

        if PortfolioName in json_object.keys():
            return {PortfolioName: json_object[PortfolioName]}
        else:
            print('The json does not contain ' + PortfolioName + ' Portfolio. Retuning -1')
            return -1

    #####################
    # ASSETS MANAGEMENT #
    #####################
    
    # Add asset to portfolio, given the PortfolioName and the Asset Dictionary - TESTED
    def AddAssetToPortfolio(self, PortfolioName, AssetDictToAdd):
        # Read the database
        json_object = self.ReadJson()

        # Check if portfolio is present in the databse
        if PortfolioName not in json_object.keys():
            print('Portfolio ' + PortfolioName + ' is not present in DB. Asset ' + list(AssetDictToAdd.keys())[0] + ' not added.')
            return
        
        # Check if the Asset in already present in the Portfolio
        if list(AssetDictToAdd.keys())[0] in json_object[PortfolioName]['Assets'].keys():
            print('The ' + list(AssetDictToAdd.keys())[0] + ' asset is already present in the ' +PortfolioName + ' portfolio. Not added.')
            return
        else:
            json_object[PortfolioName]['Assets'].update(AssetDictToAdd)
        
        # Save new json file
        self.SaveJsonFile(json_object)

    # Remove asset to portfolio - TESTED
    def RemoveAssetFromPortfolio(self, PortfolioName, AssetName):
        # Read the database
        json_object = self.ReadJson()

        # Check if portfolio is present in the databse
        if PortfolioName not in json_object.keys():
            print('Portfolio ' + PortfolioName + ' is not present in DB. Asset ' + list(AssetName.keys())[0] + ' cannot be removed.')
            return

        # Check if the Asset is present in the Portfolio
        if AssetName in json_object[PortfolioName]['Assets'].keys():
            json_object[PortfolioName]['Assets'].pop(AssetName)
        else:
            print('The ' + AssetName + ' asset is not present in the ' +PortfolioName + ' portfolio. Not removed.')
            return
            
        # Save new json file
        self.SaveJsonFile(json_object)
    
    # Initialize New Asset: Given Asset Name and Symbol it return a precompiled dictionary - TESTED
    def InitializeNewAsset(self, AssetName, AssetSymbol):
        # List which will store all the transaction for such asset
        AssetTransaction = {'Transactions' : {}}

        # Dict which will store all the statistics of such asset
        StatisticDict = {'Quantity': 0}
        StatisticDict.update({'Symbol' : AssetSymbol})
        StatisticDict.update({'AveragePrice' : 0})
        StatisticDict.update({'TotalValue' : 0})
        StatisticDict.update({'TotalProfit' : 0})
        AssetStastitics = {'Statistics' : StatisticDict}

        # Update NewAsset
        NewAsset = {AssetName : {} }
        NewAsset[AssetName].update(AssetTransaction)
        NewAsset[AssetName].update(AssetStastitics)

        return NewAsset
    
    # Modify Asset in Portfolio
    def ModifyAssetInPortfolio(self, PortfolioName, OldAssetName, AssetName, AssetSymbol):
         # Define a new dict containg the new Json
        new_dict = {}

        # Read json and iterate over it
        json_object = self.ReadJson()
        
        # Modify portfolio name and currency
        OldAsset = json_object[PortfolioName]['Assets'][OldAssetName]
        OldAsset['Statistics']['Symbol'] = AssetSymbol

        # New dictionary in input
        for AssetKey in json_object[PortfolioName]['Assets'].keys():
            if AssetKey == OldAssetName:
                new_dict.update({AssetName : OldAsset})
            else:
                new_dict.update({AssetKey:json_object[PortfolioName]['Assets'][AssetKey]})
        
        json_object[PortfolioName]['Assets'] = new_dict

        # Save new json file
        self.SaveJsonFile(json_object)
    ##########################
    # TRANSACTION MANAGEMENT #
    ##########################

    # Order the list of transaction
    def OrderTransactionList(self, TransactionDict):
        # Initialize variables
        OutDict = {}
        counter = 1

        # Reorganize json
        for key in TransactionDict.keys():
            OutDict.update({counter: TransactionDict[key]})
            counter = counter + 1

        return OutDict

     # Initialize the internal counter as the number of item in the list
    def GetTransactionCounter(self, PortfolioName, AssetName):
        # Read json and get the number opf transaction for such Asset
        json_object = self.ReadJson()

        # Update the counter
        return len(json_object[PortfolioName]['Assets'][AssetName]['Transactions'])
    
    # Concatenate Element to the json file
    def AddTransactionToAsset(self, PortfolioName, AssetName, TransactionElement):
        # Read json
        json_object = self.ReadJson()

        # Add Item independetly of the type
        self.ElementCounter = self.GetTransactionCounter(PortfolioName, AssetName) + 1
        json_object[PortfolioName]['Assets'][AssetName]['Transactions'].update({self.ElementCounter : TransactionElement})

        # Save new json file
        self.SaveJsonFile(json_object)

    # Modify a transaction in the list of transaction of a list
    def ModifyTransactionToAsset(self, ItemNum, NewList):
        # Read json
        json_object = self.ReadJson()

        if ItemNum in json_object.keys():
            json_object[ItemNum] = NewList
        
        # Save Json
        self.SaveJsonFile(json_object)

    # Remove a transaction in the list of transaction of a list
    def RemoveTransactionFromAssetList(self, ItemNum):
        # Read json
        json_object = self.ReadJson()

        if ItemNum in json_object.keys():
            json_object.pop(ItemNum)
        
        # Save Json
        self.SaveJsonFile(self.OrderList(json_object))

    # Initialize a Transaction
    def InitializeTransaction(self, Type, Date, Price, Amount, Fees, Note):
        # List which will store all the transaction for such asset
        TransactionDict = {'Type' : Type}

        # Dict which will store all the statistics of such asset
        TransactionDict.update({'Date': Date })
        TransactionDict.update({'Price' : Price})
        TransactionDict.update({'Amount' : Amount})
        TransactionDict.update({'Fees' : Fees})
        TransactionDict.update({'Note' : Note})

        return TransactionDict 

    # Compute asset statistics
    def UpdateAssetStatistics(self):
        pass

    # Read statistic of an asset in portfolio
    def ReadAssetStatistics(self):
        pass
    
    ###################################
    # PORTFOLIO STATISTICS MANAGEMENT #
    ################################### 

    # Read Statistics of Portfolio
    def ReadPortfolioStatistics(self):
        pass

    # Compute Portfolio statistics
    def UpdatePortfolioStatistics(self):
        pass