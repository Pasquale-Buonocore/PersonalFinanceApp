import Packages.DatabaseMng.AccountsManager as AccMng
import Packages.DatabaseMng.PortfolioManager as PtflMng
import Packages.DatabaseMng.PathManager as PathMng
import calendar
import os

def Update_account_database_month_year_transition(requested_month: str, requested_year: str):
    '''This function takes in input a month and updates its accounts databases starting value.
    The inputs are:
    - requested_month: given as string ex. Novomber
    - requested_year: given as a numberic string ex. 2022

    No action on the transactions.'''

    # Retrieve requested and old months database path
    requested_month_database_path, old_month_database_path = compute_requested_and_old_month_database_path(requested_month, requested_year)
    
    # if the old month does not exist, exit.
    if not os.path.exists(old_month_database_path + 'Accounts.json'): return

    # Define the two Objects
    requested_month_database_object = AccMng.AccountsManager_Class(requested_month_database_path, 'Accounts.json')
    old_month_database_object = AccMng.AccountsManager_Class(old_month_database_path, 'Accounts.json')

    # Get the json
    requested_month_database_json = requested_month_database_object.ReadJson()
    old_month_database_json = old_month_database_object.ReadJson()

    # Iterates over the account present in the previous month
    for account in old_month_database_json:
        # if not present, add the account
        if account not in requested_month_database_json.keys():

            # Define the new account to add
            AccountToAdd = requested_month_database_object.InitializeNewAccount(AccountName = account, Category = old_month_database_json[account]['Statistics']['Category'])
            requested_month_database_object.AddAccount(AccountToAdd)

        requested_month_database_json = requested_month_database_object.ReadJson()
        LastMonthSubAccountDict = {'Cash': {}, 'Assets' : {}}

        # Fill the new account with old statistics
        for subaccount in old_month_database_json[account]['SubAccount'].keys():
            for category in old_month_database_json[account]['SubAccount'][subaccount]:
                # Copy the one of the last month
                SubaccountToAdd = old_month_database_json[account]['SubAccount'][subaccount][category]

                SubaccountToAdd['MonthlyTransactions'] = {}
                if category in requested_month_database_json[account]['SubAccount'][subaccount].keys():
                    SubaccountToAdd['MonthlyTransactions'] = requested_month_database_json[account]['SubAccount'][subaccount][category]['MonthlyTransactions']
                requested_month_database_json[account]['SubAccount'][subaccount].update({category: SubaccountToAdd.copy()})

                # Update LastMontheSubAccountDict
                SubaccountToAdd.pop('MonthlyTransactions')
                LastMonthSubAccountDict[subaccount].update({category: SubaccountToAdd})
        
        requested_month_database_json[account]['Statistics']['LastMonthSubAccount'] = LastMonthSubAccountDict
        requested_month_database_object.SaveJsonFile(requested_month_database_json)

    # Update all account values before exiting
    requested_month_database_object.Update_accountDB_accounts_total_value()


def Update_transactions_database_month_year_transition(requested_month: str, requested_year: str):
    ''' This function recovers the type of earning and expences in the transition databases'''

    # Input data
    json_transactions_files = ['TransactionIn.json', 'TransactionOut.json']
    PortfoliosMap = {json_transactions_files[0]: 'IN', json_transactions_files[1]: 'OUT'}

    # Retrieve requested and old months database path
    requested_month_database_path, old_month_database_path = compute_requested_and_old_month_database_path(requested_month, requested_year) 

    # if the old month does not exist, exit.
    if not os.path.exists(old_month_database_path + 'Accounts.json'): return


    # Iterate over the json files
    for json_database_file in json_transactions_files:
        requested_month_database_object = PtflMng.PortfoliosManager_Class(requested_month_database_path, json_database_file)
        old_month_database_object = PtflMng.PortfoliosManager_Class(old_month_database_path, json_database_file)
        requested_month_database_object.CheckTransactionPortfolio(Database = requested_month_database_object, Name = PortfoliosMap[json_database_file])
        
        # Get the json
        requested_month_database_json = requested_month_database_object.ReadJson()
        old_month_database_json = old_month_database_object.ReadJson()

        # In the ['IN', 'OUT'] portfolio, if the asset is not present add it.
        for asset in old_month_database_json[PortfoliosMap[json_database_file]]['Assets'].keys():
            if asset not in requested_month_database_json:
                # Add asset to portfolio
                requested_month_database_object.AddAssetToPortfolio(PortfoliosMap[json_database_file], requested_month_database_object.InitializeNewTransactionAsset(asset))

        # Then update DesiredAssetAllocation is it is empty
        if not requested_month_database_json[PortfoliosMap[json_database_file]]['Statistics']['DesiredAssetAllocation']:
            old_month_database_json_statistics = old_month_database_json[PortfoliosMap[json_database_file]]['Statistics']['DesiredAssetAllocation']
            requested_month_database_object.UpdatePortfolioDesiredAssetAllocation(PortfoliosMap[json_database_file], old_month_database_json_statistics)

#################
###  UTILITY  ###
#################
def compute_requested_and_old_month_database_path(requested_month: str, requested_year: str):
    # Define the requested month database (if it does not exist, it will automatically be created)
    requested_month_database_path = PathMng.PathManager_Class.database_path + 'Data/' + requested_year + '/' + requested_month + '/'

    old_month, old_year = return_previous_month_year(requested_month, requested_year)
    old_month_database_path =  PathMng.PathManager_Class.database_path + 'Data/' + old_year + '/' + old_month + '/'

    return [requested_month_database_path, old_month_database_path]

def extract_previous_month_statistics(database_json, account:str) -> dict:
    tmp_statistics = database_json['account']['Statistics']

def return_previous_month_year(requested_month: str, requested_year: str) -> list:
    month_str_to_num_dict = define_str_to_num_month_dict()
    month_num_to_str_dict = define_num_to_str_month_dict()

    old_month = ''
    old_year = requested_year

    # If it is January
    if month_str_to_num_dict[requested_month] == 1:
        old_month = month_num_to_str_dict[12]
        old_year = str(int(requested_year) - 1)
    else:
        old_month = month_num_to_str_dict[month_str_to_num_dict[requested_month] - 1]

    # Return previous value
    return [old_month, old_year]

def define_str_to_num_month_dict() -> dict:
    ''' Return a dict with key == month, value == number '''
    return {month: index for index, month in enumerate(calendar.month_name) if month}

def define_num_to_str_month_dict() -> dict:
    ''' Return a dict with key == value, value == month '''
    return {mon_num: mon_str for mon_str, mon_num in {month: index for index, month in enumerate(calendar.month_name) if month}.items()}

#################
###    MAIN   ###
#################
if __name__ == '__main__':
    print('Executing some tests...')
    Update_account_database_month_year_transition('November','2022')
    Update_transactions_database_month_year_transition('November','2022')