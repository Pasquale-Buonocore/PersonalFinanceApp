from Packages.CustomFunction.GetCryptoValue import GetCryptoValue
from Packages.DatabaseMng.PathManager import *
from os.path import exists
import json
import os


###################
# CUSTOM FUNCTION #
###################
path_manager = PathManager_Class()

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

    How is the transaction dictionary composed?
    - Transactions: {
        "1":{
                Date: ---,
                PricePerCoin: ---,
                Amount: ---,
                Fees: ---,
                Note: ---,
                Status: { Open: Amount - Position closed 
                          Closed: { "1": {
                                    Date: ---,
                                    PricePerCoin: ---,
                                    Amount: ---,
                                    Fees: ---,
                                    Note: ---
                        }

                    }
                }
            }
        }
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
    
    # Initialize a new portfolio structure used in investment- TESTED
    def InitializeNewPortfolio(self, PortfolioName, PortfolioInitList = ['$', 1000, 8, 230]): 
        # A new portfolio will contains two dictionary 1) Assets and Statistics
        Asset = {'Assets': {}}

        StatisticDict = {'Currency': str(PortfolioInitList[0])}
        StatisticDict.update({'TotalValue' : int(PortfolioInitList[1])})
        StatisticDict.update({'NumberOfAssets' : int(PortfolioInitList[2])})
        StatisticDict.update({'TotalProfit' : int(PortfolioInitList[3])})
        StatisticDict.update({'ToCountInAllocation': True})
        StatisticDict.update({'ActualAssetAllocation' : {} })
        StatisticDict.update({'DesiredAssetAllocation' : {} })
        Statistic = {'Statistics' : StatisticDict }

        # Initialize dictionary with the portfolio
        NewPortfolioDict = {PortfolioName : {}}
        NewPortfolioDict[PortfolioName].update(Asset)
        NewPortfolioDict[PortfolioName].update(Statistic)
        return NewPortfolioDict

    # Initialize a new portfolio for transaction divided by category used to track expences and earning
    def InitializeTransactionPortfolio(self, PortfolioName, PortfolioInitList):
        Asset = {'Assets': {}}

        StatisticDict = {'Currency': str(PortfolioInitList[0])}
        StatisticDict.update({'NumberOfTransaction' : int(0)})
        StatisticDict.update({'TotalValue' : int(PortfolioInitList[1])})
        StatisticDict.update({'ActualAssetAllocation' : {} })
        StatisticDict.update({'DesiredAssetAllocation' : {} })
        Statistic = {'Statistics' : StatisticDict }

        # Initialize dictionary with the portfolio
        NewPortfolioDict = {PortfolioName : {}}
        NewPortfolioDict[PortfolioName].update(Asset)
        NewPortfolioDict[PortfolioName].update(Statistic)
        return NewPortfolioDict
    
    # Initialize a new portfolio for transaction list used to track expences and earning
    def InitializeTransactionListPortfolio(self, PortfolioName):
        Statistics = {'Total' : {}}

        NewPortfolioDict = {PortfolioName : {}}
        NewPortfolioDict[PortfolioName].update({'Assets' : {'Transactions' : {'Transactions' : {}} }})
        NewPortfolioDict[PortfolioName].update({'Statistics' : Statistics})

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
    
    # Initialize New Asset: Given Asset Name and Symbol it returns a precompiled dictionary - TESTED
    def InitializeNewAsset(self, AssetName, AssetSymbol):
        # List which will store all the transaction for such asset
        AssetTransaction = {'Transactions' : {}}

        # Dict which will store all the statistics of such asset
        StatisticDict = {'Quantity': 0}
        StatisticDict.update({'Symbol' : AssetSymbol})
        StatisticDict.update({'CurrentPrice' : 0})
        StatisticDict.update({'AveragePrice' : 0})
        StatisticDict.update({'TotalValue' : 0})
        StatisticDict.update({'TotalProfit' : 0})
        AssetStastitics = {'Statistics' : StatisticDict}

        # Update NewAsset
        NewAsset = {AssetName : {} }
        NewAsset[AssetName].update(AssetTransaction)
        NewAsset[AssetName].update(AssetStastitics)

        return NewAsset
    
    # Initialize New Transaction Asset: Given Asset Name it returns a precompiled dictionary of Asset
    def InitializeNewTransactionAsset(self, AssetName):
        # List which will store all the transaction for such asset
        AssetTransaction = {'Transactions' : {}}

        # Dict which will store all the statistics of such asset
        StatisticDict = {'TotalValue': 0}
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
    
    # Update the allocation of the portfolio given all the asset total value
    def UpdatePortfolioActualAssetAllocation(self, PortfolioName):
        # Read Json
        JsonFile = self.ReadJson()

        # Save the old statistics
        NewStatistics = JsonFile[PortfolioName]['Statistics']
        PortfolioTotalValue = NewStatistics['TotalValue']
        NewStatistics['ActualAssetAllocation'] = {}

        # For each asset, compute the actual % and the desired one.
        for asset in JsonFile[PortfolioName]['Assets'].keys():
            AssetStatistics = JsonFile[PortfolioName]['Assets'][asset]['Statistics']['TotalValue']
            Percentage = round(AssetStatistics/(PortfolioTotalValue + 1) * 100, 1)
            NewStatistics['ActualAssetAllocation'].update({asset : Percentage })        

        # Save new json file
        JsonFile[PortfolioName]['Statistics'] = NewStatistics
        self.SaveJsonFile(JsonFile)
    
    def UpdatePortfolioDesiredAssetAllocation(self, PortfolioName, DictDesiredAllocation = {}):
        # DictDesiredAllocation can be empty.
        # DictDesiredAllocation contains the asset as key and the allocation  % as value
        # The function has to be called also when a new asset is added in the portfolio and/or removed

        # Read Json
        JsonFile = self.ReadJson()

        # Save the old statistic
        NewStatistics = JsonFile[PortfolioName]['Statistics']
        NewDesiredUpdate = {}

        # Allocate for variable that are not in the dictionary yet
        for asset in JsonFile[PortfolioName]['Assets'].keys():
            if asset in JsonFile[PortfolioName]['Statistics']['DesiredAssetAllocation'].keys():
                NewDesiredUpdate.update({asset : JsonFile[PortfolioName]['Statistics']['DesiredAssetAllocation'][asset]})
            else:
                NewDesiredUpdate.update({asset : 0})

        # Update the current statistics
        for AssetAllocationToMod in DictDesiredAllocation.keys():
            NewDesiredUpdate.update({AssetAllocationToMod : DictDesiredAllocation[AssetAllocationToMod]})

        # Save new json file
        NewStatistics['DesiredAssetAllocation'] = NewDesiredUpdate
        JsonFile[PortfolioName]['Statistics'] = NewStatistics
        self.SaveJsonFile(JsonFile)

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
    def ModifyTransactionToAsset(self, PortfolioName = '', AssetName = '', ItemIndex = "0", NewTransaction = {}):
        # Read json
        json_object = self.ReadJson()
        new_AssetTransaction = {}
        new_Transactioncounter = 1
        for TransactionNumber in json_object[PortfolioName]["Assets"][AssetName]["Transactions"].keys():
            if TransactionNumber == ItemIndex:
                new_AssetTransaction.update({str(new_Transactioncounter) : NewTransaction})
            else:
                new_AssetTransaction.update({str(new_Transactioncounter) : json_object[PortfolioName]["Assets"][AssetName]["Transactions"][TransactionNumber]})
            
            # Update transaction counter
            new_Transactioncounter = new_Transactioncounter + 1

        # Save Json
        json_object[PortfolioName]["Assets"][AssetName]["Transactions"] = new_AssetTransaction
        self.SaveJsonFile(json_object)

    # Remove a transaction in the list of transaction of a list
    def RemoveTransactionFromAssetList(self, PortfolioName = '', AssetName = '', ItemIndex = "0"):
        # Read json
        json_object = self.ReadJson()
        new_AssetTransaction = {}
        new_Transactioncounter = 1
        for TransactionNumber in json_object[PortfolioName]["Assets"][AssetName]["Transactions"].keys():
            if TransactionNumber != ItemIndex:
                new_AssetTransaction.update({str(new_Transactioncounter) : json_object[PortfolioName]["Assets"][AssetName]["Transactions"][TransactionNumber]})
            
            # Update transaction counter
            new_Transactioncounter = new_Transactioncounter + 1

        # Save Json
        json_object[PortfolioName]["Assets"][AssetName]["Transactions"] = new_AssetTransaction
        self.SaveJsonFile(json_object)

    # Initialize a Transaction
    def InitializeTransaction(self, Date, Price, Amount, Fees, Note, PayingAccountDict, StoringAccountDict):
        # List which will store all the transaction for such asset
        TransactionDict = {'Date': Date }

        # Dict which will store all the statistics of such asset
        TransactionDict.update({'PricePerCoin' : Price})
        TransactionDict.update({'Amount' : Amount})
        TransactionDict.update({'Fees' : Fees})
        TransactionDict.update({'Note' : Note})
        TransactionDict.update({'PayingAccount' : PayingAccountDict})
        TransactionDict.update({'StoringAccount' : StoringAccountDict})

        # Initialize Status to consider Open and Closed position
        TransactionDict.update({'Status' : {'Open' : Amount, 'Closed' : {'Transactions' : {}}}})

        return TransactionDict 

    # Initialize transaction for the type income and outcome
    def InitializeNewTransactionInOut(self, Date, Quantity, Currency, Category, PaidWith, Description):

        # Dict which will store all the statistics of such asset
        TransactionDict = {'Date': Date}
        TransactionDict.update({'Amount' : Quantity})
        TransactionDict.update({'Currency' : Currency})
        TransactionDict.update({'Category' : Category})
        TransactionDict.update({'Paid with' : PaidWith})
        TransactionDict.update({'Note' : Description})

        return TransactionDict

    # Call the Update Asset Statistics for all asset
    def UpdateAllAssetStatistics(self, portfolio):
        # Read json
        json_object = self.ReadJson()

        # Update
        for AssetInPortfolio in  json_object[portfolio]['Assets']:
            self.UpdateAssetStatistics(portfolio, AssetInPortfolio)

    # Compute asset statistics - # To IMPROVE
    def UpdateAssetStatistics(self, PortfolioName, AssetName):
        return
        # Read json and get the number opf transaction for such Asset
        json_object = self.ReadJson()
        AssetDictTransaction = json_object[PortfolioName]['Assets'][AssetName]['Transactions']
        AssetDictStatistics = json_object[PortfolioName]['Assets'][AssetName]['Statistics']
        
        # Update Current Price
        AssetDictStatistics['CurrentPrice'] = GetCryptoValue(AssetName)
        AssetDictStatistics['Quantity']  = 0
        AssetDictStatistics['AveragePrice']  = 0

        for transactionIndex in AssetDictTransaction:
            # Update Holding 

            # If BUY -> SUM 
            if AssetDictTransaction[transactionIndex]['Type'] == 'BUY':
                AssetDictStatistics['Quantity'] += float(AssetDictTransaction[transactionIndex]['Amount'])
                AssetDictStatistics['AveragePrice'] += float(AssetDictTransaction[transactionIndex]['Amount']) * float(AssetDictTransaction[transactionIndex]['Price'])
            # If SELL -> SUBTRACT
            else:
                AssetDictStatistics['Quantity'] -= float(AssetDictTransaction[transactionIndex]['Amount'])
                AssetDictStatistics['AveragePrice'] -= float(AssetDictTransaction[transactionIndex]['Amount']) * float(AssetDictTransaction[transactionIndex]['Price'])

        # Update Total Value
        AssetDictStatistics['Quantity'] = round(AssetDictStatistics['Quantity'], 4)
        AssetDictStatistics['AveragePrice'] = round(AssetDictStatistics['AveragePrice'],2)
        AssetDictStatistics['TotalValue'] = round(float(AssetDictStatistics['Quantity']) * float(AssetDictStatistics['CurrentPrice']),2)

        # Update Avarage price
        try:
            AssetDictStatistics['AveragePrice'] = round(float(AssetDictStatistics['AveragePrice']) / float(AssetDictStatistics['Quantity']),2)
            AssetDictStatistics['TotalProfit'] = round(AssetDictStatistics['TotalValue'] - ( float(AssetDictStatistics['Quantity']) * float(AssetDictStatistics['AveragePrice'])), 1)
        except:
            AssetDictStatistics['AveragePrice'] = 0
            AssetDictStatistics['TotalProfit'] = 0        

        # Update json_object
        json_object[PortfolioName]['Assets'][AssetName]['Statistics'] = AssetDictStatistics
        self.SaveJsonFile(json_object)

        # Once the asset statistics are updated, update the portfolio statistics
        self.UpdatePortfolioStatistics(PortfolioName)
    
    # Update statistics for Asset in Transaction
    def UpdateAssetInTransactionStatistics(self, PortfolioName, AssetName):
        # Read json and get the number opf transaction for such Asset
        json_object = self.ReadJson()
        AssetDictTransaction = json_object[PortfolioName]['Assets'][AssetName]['Transactions']
        AssetDictStatistics = json_object[PortfolioName]['Assets'][AssetName]['Statistics']

        # Initialize Statistics Dict
        AssetDictStatistics['TotalValue'] = 0.0

        # for all transaction in AssetName, update Total Amount
        for transaction_num in AssetDictTransaction.keys():
            AssetDictStatistics['TotalValue'] += AssetDictTransaction[transaction_num]['Amount']

        # Reupdates the asset statistics
        json_object[PortfolioName]['Assets'][AssetName]['Statistics'] = AssetDictStatistics
        self.SaveJsonFile(json_object)

        self.UpdateTransactionPortfolio(PortfolioName)

    ###################################
    # PORTFOLIO STATISTICS MANAGEMENT #
    ################################### 

    # Call the Update Portfolio Statistics for all asset
    def UpdateAllPortfolioStatistics(self):
        # Read json
        json_object = self.ReadJson()

        # Update
        for Portfolio in  json_object.keys():
            self.UpdatePortfolioStatistics(Portfolio)

    # Compute Portfolio statistics
    def UpdatePortfolioStatistics(self, Portfolio):
        # Read json and get the number opf transaction for such Asset
        json_object = self.ReadJson()
        
        # Update number of asset
        json_object[Portfolio]['Statistics']['NumberOfAssets'] = len(json_object[Portfolio]['Assets'].keys())
        json_object[Portfolio]['Statistics']['TotalValue'] = 0
        json_object[Portfolio]['Statistics']['TotalProfit'] = 0

        for asset in json_object[Portfolio]['Assets'].keys():
            # Update total value
            json_object[Portfolio]['Statistics']['TotalValue'] += json_object[Portfolio]['Assets'][asset]['Statistics']['TotalValue']
            # Update total profit
            json_object[Portfolio]['Statistics']['TotalProfit'] += json_object[Portfolio]['Assets'][asset]['Statistics']['TotalProfit']

        json_object[Portfolio]['Statistics']['TotalValue'] = round(json_object[Portfolio]['Statistics']['TotalValue'], 2)
        json_object[Portfolio]['Statistics']['TotalProfit'] = round(json_object[Portfolio]['Statistics']['TotalProfit'], 2)

        self.SaveJsonFile(json_object)

    # Call the Update Portfolio Statistics for all transaction Portfolio
    def UpdateAllTransactionPortfolioStatistics(self):
        # Read json
        json_object = self.ReadJson()

        # Update
        for Portfolio in  json_object.keys():
            self.UpdateTransactionPortfolio(Portfolio)

    # Update Portfolio of transaction
    def UpdateTransactionPortfolio(self, Portfolio):
        # Read json and get the number opf transaction for such Asset
        json_object = self.ReadJson()

        # I need to update:
        # 1. Number of transaction
        # 2. Total amount Spent/Earned
        # 3. Update the actual allocation (not in %)
        json_object[Portfolio]['Statistics']['NumberOfTransaction'] = 0
        json_object[Portfolio]['Statistics']['TotalValue'] = 0
        json_object[Portfolio]['Statistics']['ActualAssetAllocation'] = {}

        for asset in json_object[Portfolio]['Assets'].keys():
            # Update the total number of transaction
            json_object[Portfolio]['Statistics']['NumberOfTransaction'] += int(len(json_object[Portfolio]['Assets'][asset]['Transactions']))

            # Update the asset value to total value of the portfolio
            json_object[Portfolio]['Statistics']['TotalValue'] += float(json_object[Portfolio]['Assets'][asset]['Statistics']['TotalValue'])

            # Append the total expence/earning for such category in the portfolio statistics
            json_object[Portfolio]['Statistics']['ActualAssetAllocation'].update({asset : float(json_object[Portfolio]['Assets'][asset]['Statistics']['TotalValue'])})

            if asset not in json_object[Portfolio]['Statistics']['DesiredAssetAllocation'].keys(): json_object[Portfolio]['Statistics']['DesiredAssetAllocation'] .update({asset : 0})

        self.SaveJsonFile(json_object)