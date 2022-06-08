import Packages.DatabaseMng.DatabaseMng as db_manager

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