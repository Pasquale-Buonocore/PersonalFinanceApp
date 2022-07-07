import Packages.CustomItem.WarningPopup as Wrn_popup
from kivy.uix.popup import Popup
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/TransactionCategoryListPopup.kv')

class TransactionCategoryListPopup(Popup):
    def __init__(self, transaction_type = 'IN'):
        # Initialize the super class
        super().__init__(title = 'TRANSACTION ' + transaction_type + ' CLASSES', size_hint = (0.3,0.7))

        # Define inner attributes
        self.type = transaction_type if type in ['IN','OUT'] else 'IN'

        # Save item to modify
        self.PopulateListOfClasses(self.type)


    def PopulateListOfClasses(self, transaction_type = 'IN'):
        # Modify text input if itemToMod is not empty
        return

    def RemoveClass(self):
        pass

    def Confirm(self, App):
        return

        # Keep the boolean error
        string = ''

        # Retrive data "Portfolio Name" from Text Input - In empty do nothing
        PortfolioName = self.ids["PortfolioName"].text.strip().upper()
        if not PortfolioName: string = string + 'ERROR: Empty asset name FIELD'

        # Retrive data "Currency Value" from Text Input - In empty do nothing
        CurrencySymbol = self.ids["CurrencyValue"].text.strip().upper()
        if not CurrencySymbol: string = string + '\nERROR: Empty symbol value FIELD'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
        else:
            # Instantiate Screen and Json manager
            ActualScreen = App.root.children[0].children[0].children[0]
            DBManager = ActualScreen.DBManager

            # Define Portfolio To Add
            PortfolioToAdd = DBManager.InitializeNewPortfolio(PortfolioName,[CurrencySymbol,0,0,0])
            
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                DBManager.ModifyPortfolio(list(self.itemToMod.keys())[0], PortfolioName, CurrencySymbol)
            else:
                # Check if the Portfolio already exists
                PortfolioAlreadyPresent = list(DBManager.ReadJson().keys())
                if PortfolioName in PortfolioAlreadyPresent:
                    # Show a warning message
                    string = 'The portfolio ' + PortfolioName + ' already exists.\n It cannot be added. Remove it first!'
                    Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
                    Pop.open()
                else:
                    # Append new item
                    DBManager.AddPortfolio(PortfolioToAdd)

            # Update the Json and Update the Dashboard Screen
            ActualScreen.UpdateScreen(ActualScreen.ScreenName, ActualScreen.PortfolioJsonPath)

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()