from kivy.lang import Builder
from kivy.uix.popup import Popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/RemoveTransactionInOutPopup.kv')

class RemoveTransactionInOutPopup(Popup):
    def __init__(self, title_str, PortfolioName, AssetName, TransactionIndex, DBManager, ManagerOfScreen):
        super().__init__(title = title_str, size_hint = (0.3,0.5))
        self.ManagerOfScreen = ManagerOfScreen
        self.PortfolioName = PortfolioName # contains the Portfolio Name that contains the Asset
        self.AssetName = AssetName # Asset Name
        self.DBManager = DBManager # Database
        self.TransactionIndex = TransactionIndex


    def RemoveIt(self):

        # Remove widget from the Json and update Asset Statistics
        self.DBManager.RemoveTransactionFromAssetList(self.PortfolioName, self.AssetName, self.TransactionIndex)
        self.DBManager.UpdateAssetInTransactionStatistics(self.PortfolioName, self.AssetName)

        # Update the UI
        self.ManagerOfScreen.UpdateScreen(self.PortfolioName, self.DBManager)

        # Close the popup
        self.dismiss()