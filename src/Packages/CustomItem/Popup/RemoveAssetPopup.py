from kivy.lang import Builder
from kivy.uix.popup import Popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/RemoveAssetPopup.kv')

class RemoveAssetPopup(Popup):
    def __init__(self, title_str, PortfolioName, AssetName, DBManager, Screen, FromScreenName):
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        self.FromScreenName = FromScreenName # contains the screenName where the Portfolio was opened
        self.PortfolioName = PortfolioName # contains the Portfolio Name that contains the Asset
        self.ManagerOfScreen = Screen # Scrren 'ASSETS'
        self.AssetName = AssetName # Asset Name
        self.DBManager = DBManager # Database


    def RemoveIt(self):

        # Remove widget from the Json
        self.DBManager.RemoveAssetFromPortfolio(self.PortfolioName, self.AssetName)

        # Update the UI
        self.ManagerOfScreen.UpdateScreen(self.FromScreenName, self.PortfolioName)

        # Close the popup
        self.dismiss()