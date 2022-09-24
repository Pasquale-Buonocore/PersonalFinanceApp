from xmlrpc.client import boolean
import Packages.DatabaseMng.PortfolioManager as db_manager
import re

# Constant
PAYING_ACCOUNT_LIST_ELEMENT_MAX_LENGTH = 3

# Return the database to use according to the Screen selected
def ReturnJsonPathGivenScreenName(ScreenName):
    if ScreenName == 'ETF - ETC':
        return db_manager.path_manager.ETF_ETC_path
    if ScreenName == 'STOCKS':
        return db_manager.path_manager.Stocks_path
    if ScreenName == 'BONDS':
        return db_manager.path_manager.Bonds_path
    if ScreenName == 'COMMODITIES':
        return db_manager.path_manager.Commodities_path
    if ScreenName == 'CRYPTO':
        return db_manager.path_manager.Crypto_path


def verify_numeric_float_string(numeric_string):
    non_decimal = re.compile(r'[^\d.]+')

    # first substitute ',' with '.'
    numeric_string = non_decimal.sub('', numeric_string)

    counter = numeric_string.count('.')
    while counter > 1:
        numeric_string = numeric_string.replace('.','',1)
        counter = numeric_string.count('.')
    
    return numeric_string


def check_if_balance_is_not_enough(available_amount: float, transaction_amount: float) -> boolean:
    ''' return 1 if available balance is smaller then transaction value'''
    return 1 if float(available_amount) < float(transaction_amount) else 0


def return_account_dict_given_account_element_list(three_element_list: list) -> dict:
    Transaction_PayingAccountKey = ['Account', 'SubAccount', 'Currency']
    Transaction_PayingAccountValue = [element.strip() for element in three_element_list.split('-')]

    if len(Transaction_PayingAccountValue) > PAYING_ACCOUNT_LIST_ELEMENT_MAX_LENGTH: return
    return dict(zip(Transaction_PayingAccountKey,Transaction_PayingAccountValue))