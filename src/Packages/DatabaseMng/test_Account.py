import AccountsManager as AccMng
from PathManager import *
path_manager = PathManager_Class()

# Initialize New Account Class
DBManager = AccMng.AccountsManager_Class(path_manager.database_path, path_manager.Accounts_path)

# Add New Account
LastMonthSubAccount = {'Cash' : {'USD':{'Amount': 200, 'Currency' : '$'}, 'EURO': {'Amount': 150, 'Currency': '€'}}}
LastMonthSubAccount.update({'Assets': {}})
NewAccount = DBManager.InitializeNewAccount(AccountName = 'Unicredit Bank', Category = 'Bank Account', Currency = '€', LastMonthSubAccount = LastMonthSubAccount, LastMonthValue = 350)
DBManager.AddAccount(NewAccount)

# Remove Account
# DBManager.RemoveAccount(AccountName = 'Unicredit Bank')

# Update Cash
DBManager.UpdateCashSubAccountCategory(AccountName = 'Unicredit Bank', CashCategory = 'RUBLO', DictOfParameters = {'Amount' : 1900})

# Add new type of Cash
# DBManager.AddCashSubAccountCategory(AccountName = 'Unicredit Bank', CashCategory = 'RUBLO', Amount = 100, Currency = 'R')

# Update Asset
DBManager.UpdateAssetSubAccountCategory(AccountName = 'Unicredit Bank', AssetCategory = 'APPL Stock', DictOfParameters = {'Amount': 5, 'TotalValue' : 1300})

# Add Asset
# DBManager.AddAssetSubAccountCategory(AccountName = 'Unicredit Bank' , AssetCategory = 'APPL Stock', Amount = 3, TotalValue = 1100, Symbol = 'APPL', Currency = '$')

