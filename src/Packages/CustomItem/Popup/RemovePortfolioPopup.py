from kivy.lang import Builder
from kivy.uix.popup import Popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/RemovePortfolioPopup.kv')

class RemovePortfolioPopup(Popup):
    def __init__(self, title_str, PortfolioName, DBManager, Screen):
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        self.ManagerOfScreen = Screen
        self.PortfolioName = PortfolioName
        self.DBManager = DBManager

    def RemoveIt(self):

        # Remove widget from the Json
        self.DBManager.RemovePortfolio(self.PortfolioName)

        # Update the UI
        self.ManagerOfScreen.UpdateScreen(self.ManagerOfScreen.ScreenName, self.ManagerOfScreen.PortfolioJsonPath)

        # Close the popup
        self.dismiss()