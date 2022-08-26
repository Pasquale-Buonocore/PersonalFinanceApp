from kivy.lang import Builder
from kivy.uix.popup import Popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/RemoveTransactionPopup.kv')

class RemoveTransactionPopup(Popup):
    def __init__(self, title_str, PortfolioName, AssetName, TransactionIndex, DBManager, Screen, FromScreenName):
        super().__init__(title = title_str, size_hint = (0.3,0.5))
        self.FromScreenName = FromScreenName # contains the screenName where the Portfolio was opened
        self.PortfolioName = PortfolioName # contains the Portfolio Name that contains the Asset
        self.ManagerOfScreen = Screen # Scrren 'ASSETS'
        self.AssetName = AssetName # Asset Name
        self.DBManager = DBManager # Database
        self.TransactionIndex = TransactionIndex


    def RemoveIt(self):

        # Remove widget from the Json and update Asset Statistics
        self.DBManager.RemoveTransactionFromAssetList(self.PortfolioName, self.AssetName, self.TransactionIndex)
        self.DBManager.UpdateAssetStatistics(self.PortfolioName, self.AssetName)

        # Update the UI
        self.ManagerOfScreen.UpdateScreen(self.AssetName, self.PortfolioName, self.FromScreenName)

        # Close the popup
        self.dismiss()