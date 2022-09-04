import Packages.DatabaseMng.PortfolioManager as db_manager
import re

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