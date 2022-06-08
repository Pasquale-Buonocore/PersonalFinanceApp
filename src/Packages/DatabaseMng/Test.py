from DatabaseMng import * 

#########
# TESTS #
#########
TEST_TYPE = 2 # 0 for dictionary, 1 for list, 2 for Portfolios

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
    elif TEST_TYPE == 2:
        # Try to create a portfolio
        Manager = PortfoliosManager_Class(PathManager.database_path, PathManager.Crypto_path)

        # Add a new portfolio
        PortfolioToAdd = Manager.InitializeNewPortfolio('MAIN PAC', PortfolioInitList = ['$', 500 , 2, -200])
        Manager.AddPortfolio(PortfolioToAdd)
        PortfolioToAdd = Manager.InitializeNewPortfolio('AIRDROPS')
        Manager.AddPortfolio(PortfolioToAdd)
        PortfolioToAdd = Manager.InitializeNewPortfolio('STABLE COINS', PortfolioInitList = ['$', 1000 , 2, 0])
        Manager.AddPortfolio(PortfolioToAdd)

        # Remove a Portfolio
        Manager.RemovePortfolio('PINCOPALLO')

        # Substitute Portfolio
        PortfolioToAdd = Manager.ReadPortfolio('MAIN PAC')
        PortfolioToAdd['MAIN PAC']['Statistics']['NumberOfAssets'] = 1
        Manager.SubstitutePortfolio(PortfolioToAdd)

        # Add Asset to Portfolio PortfolioName
        MainPortfolio = Manager.ReadPortfolio('MAIN PAC')
        AssetToAdd_btc = Manager.InitializeNewAsset('Bitcoin', 'BTC')
        AssetToAdd_egld = Manager.InitializeNewAsset('Elrond', 'EGLD')
        Manager.AddAssetToPortfolio(PortfolioName = 'MAIN PAC', AssetDictToAdd = AssetToAdd_btc)
        Manager.AddAssetToPortfolio(PortfolioName = 'MAIN PAC', AssetDictToAdd = AssetToAdd_egld)

        # Remove Asset to Portfolio
        # Manager.RemoveAssetFromPortfolio(PortfolioName = 'MAIN PAC', AssetName = 'Elrond')
        # Manager.RemoveAssetFromPortfolio(PortfolioName = 'MAIN PAC', AssetName = 'Bitcoin')

        print('**** END ****')


