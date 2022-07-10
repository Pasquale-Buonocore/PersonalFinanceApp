from kivy.lang import Builder
from kivy.uix.popup import Popup
import Packages.CustomItem.WarningPopup as Wrn_popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/RemoveClassPopup.kv')

class RemoveClassPopup(Popup):
    def __init__(self, portfolio, asset, DBManager):
        super().__init__(title = 'REMOVE CLASS IN TRANSACTION ' + portfolio, size_hint = (0.3,0.5))
        self.portfolio = portfolio
        self.DBManager = DBManager
        self.asset = asset

    def RemoveIt(self, App):
        
        # Once the Remove button has been pressed, check if there are transaction within this class
        if len(self.DBManager.ReadJson()[self.portfolio]['Assets'][self.asset]['Transactions'].keys()):
            # Class cannot be removed because there are transaction in
            string = self.asset + ' class cannot be removed.\nIt\'s total value is not zero.\n'
            string = string + 'Proceed removing all its transaction first.'
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string)
            Pop.open()

            # Close the popup after confirmation
            self.dismiss()
        # If the class has no transactions, clear it and update portfolio statistics
        else:
            ActualScreen = App.root.children[0].children[0].children[0]

            # Remove widget from the Json and update Asset Statistics
            self.DBManager.RemoveAssetFromPortfolio(self.portfolio, self.asset)
            self.DBManager.UpdatePortfolioActualAssetAllocation(self.portfolio)
            self.DBManager.UpdatePortfolioDesiredAssetAllocation(self.portfolio)

            # Update the opened popup
            self.parent.children[1].PopulateListOfClasses()

            # Update the Transaction Screen
            ActualScreen.UpdateScreen()

            # Close the popup
            self.dismiss()