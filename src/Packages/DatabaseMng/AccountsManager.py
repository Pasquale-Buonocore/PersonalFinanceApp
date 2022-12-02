
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
    def AddAccount(self, NewAccount):
        # Read json
        json_object = self.ReadJson()
            
        # Add items in dictionary if not already present
        for key in NewAccount.keys():
            if key not in json_object.keys():
                json_object.update({key : NewAccount[key]})            
        
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
    def InitializeNewAccount(self, AccountName, Category, LastMonthValue = 0, LastMonthSubAccount = {'Cash': {}, 'Assets' : {}}):
        NewAccountDict = {}

        # Add the SubAccount section
        NewAccountDict.update({'SubAccount': self.InitializeNewSubAccount(LastMonthSubAccount)})
        # Add the Statistics section
        NewAccountDict.update({'Statistics': self.InitializeNewAccountStatistics(Category, LastMonthSubAccount, LastMonthValue)})

        self.UpdateActualMonthAccountValue(AccountName)

        return {AccountName : NewAccountDict}

    # Return a dict with "cash" and "Asset" subaccount - TESTED
    def InitializeNewSubAccount(self, LastMonthSubAccount = {}):
        if LastMonthSubAccount: return LastMonthSubAccount

        return {'Cash': {}, 'Assets': {}}

    # Initialize a dict with new account statistics
    def InitializeNewAccountStatistics(self, Category, LastMonthSubAccount, LastMonthValue):
        StatisticsDict =  {'Category': Category}
        StatisticsDict.update({'LastMonthSubAccount' : LastMonthSubAccount})
        StatisticsDict.update({'LastMonthValue' : LastMonthValue})
        StatisticsDict.update({'ActualMonthValue' : LastMonthValue})
        
        return StatisticsDict
 
    # Update the current Value of the Account
    def UpdateActualMonthAccountValue(self, AccountName):
        pass
    
    ###########################
    # SUBACCOUNTS MANAGEMENTS #
    ###########################

    # Add a cash subaccount category - TESTED
    def AddCashSubAccountCategory(self, AccountName, CashCategory, Symbol, BasedCarrency, InitialLiquidity = 0):
        # Read json
        json_object = self.ReadJson()
        
        if AccountName not in json_object.keys(): 
            print('The '+ AccountName + ' account does not exist and it is not possible to update its assets. Exiting...')
            return

        if CashCategory in json_object[AccountName]['SubAccount']['Cash'].keys():
            print('The '+ CashCategory + ' cash category already exist. Use the "UpdateCashSubAccount" function to modify it. Exiting...')
            return

        CashDictionary = {'TotalValue' : InitialLiquidity}
        CashDictionary.update({'Symbol' : Symbol})
        CashDictionary.update({'BasedCurrency' : BasedCarrency})
        CashDictionary.update({'LiquidityContribution' : float(InitialLiquidity)})
        CashDictionary.update({'InvestmentContribution' : float(0)})
        CashDictionary.update({'MonthlyTransactions' : {}})

        json_object[AccountName]['SubAccount']['Cash'].update({CashCategory : CashDictionary})

        # Save new json file
        self.SaveJsonFile(json_object)

    # Add an Asset category - TESTED
    def AddAssetSubAccountCategory(self, AccountName, AssetCategory, Symbol, InitialLiquidity = 0):
        # Read json
        json_object = self.ReadJson()
        
        if AccountName not in json_object.keys(): 
            print('The '+ AccountName + ' account does not exist and it is not possible to update its assets. Exiting...')
            return

        if AssetCategory in json_object[AccountName]['SubAccount']['Assets'].keys():
            print('The '+ AssetCategory + ' cash category already exist. Use the "UpdateAssetSubAccount" function to modify it. Exiting...')
            return
    
        AssetDictionary = {'TotalValue' : InitialLiquidity}
        AssetDictionary.update({'Symbol' : Symbol})
        AssetDictionary.update({'LiquidityContribution' : float(InitialLiquidity)})
        AssetDictionary.update({'InvestmentContribution' : float(0)})
        AssetDictionary.update({'MonthlyTransactions' : {}})
        json_object[AccountName]['SubAccount']['Assets'].update({AssetCategory: AssetDictionary})

        # Save new json file
        self.SaveJsonFile(json_object)

    # Append a transaction in the transaction list of the AccountName, [Cash, Asset], Asset  - TESTED
    def AppendTransactionToList(self, AccountName, cash_or_asset, AssetName, TransactionToAppendDict) -> int:
        # Read json
        json_object = self.ReadJson()

        if AccountName not in json_object.keys(): 
            print('The '+ AccountName + ' account does not exist and it is not possible to update its assets. Exiting...')
            return -1

        if cash_or_asset not in json_object[AccountName]['SubAccount'].keys():
            print('Neither Cash not Asset was added. Exiting...')
            return -1

        if AssetName not in json_object[AccountName]['SubAccount'][cash_or_asset].keys():
            print('The '+ AssetName + ' cash category does not exist and it is not possible to be updated. Exiting...')
            return -1
        
        if list(TransactionToAppendDict.keys())[0] in json_object[AccountName]['SubAccount'][cash_or_asset][AssetName]['MonthlyTransactions']:
            print('This code already exist and the transaction cannot be added. Exiting...')
            return 1
        
        json_object[AccountName]['SubAccount'][cash_or_asset][AssetName]['MonthlyTransactions'].update(TransactionToAppendDict)
 
        # Save new json file
        self.SaveJsonFile(json_object)

    # Remove transaction knowing Account, SubAccount and Currency based on Linking Code
    def RemoveMonthlyTransactionBasedOnLinkingCode(self, AccountName = '', SubAccountName = '', CurrencyName = '', LinkingCode = '') -> None:
        # Read json
        json_object = self.ReadJson()

        if LinkingCode in json_object[AccountName]["SubAccount"][SubAccountName][CurrencyName]['MonthlyTransactions'].keys(): 
            json_object[AccountName]["SubAccount"][SubAccountName][CurrencyName]['MonthlyTransactions'].pop(LinkingCode)
        
        # Save json
        self.SaveJsonFile(json_object)

    ###################
    # Statistic Value #
    ###################
    # Initialize transaction for the type income and outcome
    def Initialize_investiment_transaction_to_store_into_account(self, Date, Quantity, Category, Portfolio, Description):

        # Dict which will store all the statistics of such asset
        TransactionDict = {'Date': Date}
        TransactionDict.update({'Amount' : Quantity})
        TransactionDict.update({'Category' : Category})
        TransactionDict.update({'Investment_location' : Portfolio})
        TransactionDict.update({'Note' : Description})

        return TransactionDict

    def Update_Account_Statistics(self):
        # Read json
        json_object = self.ReadJson()

        # Iterate over all account
        for accounts in json_object:
            # Iterates over all subaccounts
            tmp_total_amount = 0.0
            for subaccounts in json_object[accounts]['SubAccount']:
                # Iterate over currencies
                for currency in json_object[accounts]['SubAccount'][subaccounts]:
                    # Improve such part, there will be a conversion base on the currency
                    tmp_total_amount += round(float(json_object[accounts]['SubAccount'][subaccounts][currency]['TotalValue']),2)
                
            # Once iterate over all the currency in the subaccounts, save ActualMonthValue and LastMonthValue
            json_object[accounts]['Statistics']['ActualMonthValue'] = tmp_total_amount
            
            tmp_total_amount = 0.0
            for subaccount in json_object[accounts]['Statistics']['LastMonthSubAccount']:
                for currency in json_object[accounts]['Statistics']['LastMonthSubAccount'][subaccount]:
                        tmp_total_amount += round(float(json_object[accounts]['Statistics']['LastMonthSubAccount'][subaccount][currency]['TotalValue']),2)
            
            json_object[accounts]['Statistics']['LastMonthValue'] = tmp_total_amount

            # Save new json file
            self.SaveJsonFile(json_object)

            # Read json
            json_object = self.ReadJson()


    def Update_accountDB_accounts_total_value(self):
        ''' This function iterates over all the account in the accountDB and update'''
        # Read json
        json_object = self.ReadJson()

        for account in json_object:
            for subaccount in json_object[account]['SubAccount']:
                for currency in json_object[account]['SubAccount'][subaccount]:
                    self.Update_liquid_investing_balance(account, subaccount, currency)
        
        self.Update_Account_Statistics()

    def Update_liquid_investing_balance(self, Account, SubAccount, Currency) -> None:
        '''This function uses the transaction in the monthly transaction dictionary to update liquidity and investiment.
        It is defined to update them for a currency only'''

        # Read json
        json_object = self.ReadJson()

        if Account not in json_object.keys(): 
            print('The '+ Account + ' account does not exist and it is not possible to update its assets. Exiting...')
            return -1

        if SubAccount not in ['Cash', 'Assets']:
            print('The '+ SubAccount + ' account does not exist and it is not possible to update its assets. Exiting...')
            return -1

        if Currency not in json_object[Account]['SubAccount'][SubAccount].keys(): 
            print('The '+ Currency + ' account does not exist and it is not possible to update its assets. Exiting...')
            return -1

        # Extract the last month end value for Liquidity and Investment contribution
        Liquidity_Contribution_init = float(json_object[Account]['Statistics']['LastMonthSubAccount'][SubAccount][Currency]['LiquidityContribution']) if (Currency in json_object[Account]['Statistics']['LastMonthSubAccount'][SubAccount].keys()) else 0.0
        Investment_Contribution_init = float(json_object[Account]['Statistics']['LastMonthSubAccount'][SubAccount][Currency]['InvestmentContribution']) if (Currency in json_object[Account]['Statistics']['LastMonthSubAccount'][SubAccount].keys()) else 0.0
        
        for transaction_key in json_object[Account]['SubAccount'][SubAccount][Currency]['MonthlyTransactions']:
 
            # The transaction key respects a certain format and needs to be understood!
            transaction = json_object[Account]['SubAccount'][SubAccount][Currency]['MonthlyTransactions'][transaction_key]

            #############################
            # TRANSACTION IN OUT SCREEN #
            #############################
            # SS -> Spent standard (the Liquidity Contribution amount needs to be detracted of the current amount)
            if transaction_key[0:2] == 'SS': Liquidity_Contribution_init -= transaction['Amount']

            # ES -> Earning standard (the Liquidity Contribution amount needs to be added of the current amount)
            if transaction_key[0:2] == 'ES': Liquidity_Contribution_init += transaction['Amount']

            #####################
            # INVESTMENT SCREEN #
            #####################

            # OI -> Open Investment position (the Liquidity Contribution amount needs to be detracted of the current amount)
            # I can create a portfolio using as base curreny cash or asset. The constraint is that only Liquid cash/asset can be used.
            # This constraint must be set in the GUI (as it is now)
            if transaction_key[0:2] == 'OI': Liquidity_Contribution_init -= transaction['Amount']

            # CI -> Close Investment position (the Liquidity Contribution amount needs to be added of the current amount)
            # When an investment position is closed, the liquidity obtained must be store somewhere.
            # It can be stored both in cash/asset with the constraint to store it in the liquidity part
            if transaction_key[0:2] == 'CI': Liquidity_Contribution_init += transaction['Amount']

            # SI -> Store Investment (the Investment Contribution amount needs to be added to the current amount)
            # When a new position is open, what it is bought must bne stored. It can be stored as cash/asset but in the investment section. 
            if transaction_key[0:2] == 'SI': Investment_Contribution_init += transaction['Amount']

            # DI -> Destore Investment (the Investment Contribution amount needs to be detracted to the current amount)
            # When a position is closed, the amount stored in the investment part must be removed.
            if transaction_key[0:2] == 'DI': Investment_Contribution_init -= transaction['Amount']


        # Once all the transactions for that currency has been transacted, update the json and save it
        json_object[Account]['SubAccount'][SubAccount][Currency]['LiquidityContribution'] = Liquidity_Contribution_init
        json_object[Account]['SubAccount'][SubAccount][Currency]['InvestmentContribution'] = Investment_Contribution_init

        # Then update the Total value for such asset/cash
        json_object[Account]['SubAccount'][SubAccount][Currency]['TotalValue'] = Liquidity_Contribution_init + Investment_Contribution_init
        
        # Save new json file
        self.SaveJsonFile(json_object)
