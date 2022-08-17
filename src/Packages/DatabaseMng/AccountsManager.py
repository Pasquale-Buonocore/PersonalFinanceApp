
from os.path import exists
import json

###################
# CUSTOM FUNCTION #
###################

class AccountsManager_Class():
    """ The json contains several Portfolios, which are organized as:

    Account (Name)
        - SubAccount
            - Cash # dict of different type of cash
                     ex. {Euro: {Value : X, Currency: XX}, USD: {Value: Y, Currency : YY}}

            - Asset # dict of different type of asset
                     ex. {Bitcoin: {Amount: X, TotalValue: Y, Symbol: YYY, Currency = $}}
                    
        - Statistics
            - Category (Bank Account, Ex)
            - Last Month SubAccount
            - Last Month value
            - Actual value
            - Currency

    There might be more than one account
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

    #######################
    # ACCOUNTS MANAGEMENT #
    #######################

    # Add Account to the Json File - TESTED
    def AddAccount(self, dictionary):
        # Read json
        json_object = self.ReadJson()
            
        # Add items in dictionary if not already present
        for key in dictionary.keys():
            if key not in json_object.keys():
                json_object.update({key : dictionary[key]})            
        
        # Save new json file
        self.SaveJsonFile(json_object)

    # Remove Account from the Json - TESTED
    def RemoveAccount(self, AccountName):
        # Read json
        json_object = self.ReadJson()

        # Remove Item
        if AccountName in json_object.keys():
            json_object.pop(AccountName)

        # Save new Json file
        self.SaveJsonFile(json_object)

    # Initialize a New Account returning a dict - TESTED
    def InitializeNewAccount(self, AccountName, Category, Currency = '$', LastMonthValue = 0, LastMonthSubAccount = {}):
        NewAccountDict = {}

        # Add the SubAccount section
        NewAccountDict.update({'SubAccount': self.InitializeNewSubAccount(LastMonthSubAccount)})
        # Add the Statistics section
        NewAccountDict.update({'Statistics': self.InitializeNewAccountStatistics(Category, Currency, LastMonthSubAccount, LastMonthValue)})

        self.UpdateActualMonthAccountValue(AccountName)

        return {AccountName : NewAccountDict}

    # Return a dict with "cash" and "Asset" subaccount - TESTED
    def InitializeNewSubAccount(self, LastMonthSubAccount = {}):
        if LastMonthSubAccount:
            return LastMonthSubAccount

        return {'Cash': {}, 'Assets': {}}

    # Initialize a dict with new account statistics
    def InitializeNewAccountStatistics(self, Category, Currency, LastMonthSubAccount, LastMonthValue):
        StatisticsDict =  {'Category': Category}
        StatisticsDict.update({'LastMonthSubAccount' : LastMonthSubAccount})
        StatisticsDict.update({'LastMonthValue' : LastMonthValue})
        StatisticsDict.update({'ActualMonthValue' : LastMonthValue})
        StatisticsDict.update({'Currency' : Currency})
        
        return StatisticsDict

    # Update the current Value of the Account
    def UpdateActualMonthAccountValue(self, AccountName):
        pass

    ###########################
    # SUBACCOUNTS MANAGEMENTS #
    ###########################

    # Add a cash subaccount category - TESTED
    def AddCashSubAccountCategory(self, AccountName, CashCategory, Amount, Currency):
        # Read json
        json_object = self.ReadJson()
        
        if AccountName not in json_object.keys(): 
            print('The '+ AccountName + ' account does not exist and it is not possible to update its assets. Exiting...')
            return

        if CashCategory in json_object[AccountName]['SubAccount']['Cash'].keys():
            print('The '+ CashCategory + ' cash category already exist. Use the "UpdateCashSubAccount" function to modify it. Exiting...')
            return
 
        json_object[AccountName]['SubAccount']['Cash'].update({CashCategory: {'Amount' : Amount, 'Currency' : Currency}})

        # Save new json file
        self.SaveJsonFile(json_object)

    # Update the an asset in the cash subaccount - TESTED
    def UpdateCashSubAccountCategory(self, AccountName, CashCategory, DictOfParameters):
        # Read json
        json_object = self.ReadJson()

        if AccountName not in json_object.keys(): 
            print('The '+ AccountName + ' account does not exist and it is not possible to update its assets. Exiting...')
            return

        if CashCategory not in json_object[AccountName]['SubAccount']['Cash'].keys():
            print('The '+ CashCategory + ' cash category does not exist and it is not possible to be updated. Exiting...')
            return
        
        for parameter in DictOfParameters.keys():
            if parameter in json_object[AccountName]['SubAccount']['Cash'][CashCategory].keys():
                json_object[AccountName]['SubAccount']['Cash'][CashCategory][parameter] = DictOfParameters[parameter]
            else:
                print('The ' + parameter + ' parameter passed does not exist and cannot be updated.')
 
        # Save new json file
        self.SaveJsonFile(json_object)

    # Add an Asset category - TESTED
    def AddAssetSubAccountCategory(self, AccountName, AssetCategory, Amount, TotalValue, Symbol, Currency):
        # Read json
        json_object = self.ReadJson()
        
        if AccountName not in json_object.keys(): 
            print('The '+ AccountName + ' account does not exist and it is not possible to update its assets. Exiting...')
            return

        if AssetCategory in json_object[AccountName]['SubAccount']['Assets'].keys():
            print('The '+ AssetCategory + ' cash category already exist. Use the "UpdateAssetSubAccount" function to modify it. Exiting...')
            return
 
        json_object[AccountName]['SubAccount']['Assets'].update({AssetCategory: {'Amount' : Amount, 'TotalValue': TotalValue, 'Symbol' : Symbol,'Currency' : Currency}})

        # Save new json file
        self.SaveJsonFile(json_object)

    # Update ad Asset category 
    def UpdateAssetSubAccountCategory(self, AccountName, AssetCategory, DictOfParameters):
        # Read json
        json_object = self.ReadJson()

        if AccountName not in json_object.keys(): 
            print('The '+ AccountName + ' account does not exist and it is not possible to update its assets. Exiting...')
            return

        if AssetCategory not in json_object[AccountName]['SubAccount']['Assets'].keys():
            print('The '+ AssetCategory + ' cash category does not exist and it is not possible to be updated. Exiting...')
            return
        
        for parameter in DictOfParameters.keys():
            if parameter in json_object[AccountName]['SubAccount']['Assets'][AssetCategory].keys():
                json_object[AccountName]['SubAccount']['Assets'][AssetCategory][parameter] = DictOfParameters[parameter]
            else:
                print('The ' + parameter + ' parameter passed does not exist and cannot be updated.')
        
        # Save new json file
        self.SaveJsonFile(json_object)

