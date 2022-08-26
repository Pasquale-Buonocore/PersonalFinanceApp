from kivy.lang import Builder
from kivy.uix.popup import Popup
import Packages.CustomItem.Popup.WarningPopup as Wrn_popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddPortfolioPopup.kv')

class AddPortfolioPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint = (0.3,0.5))

        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        ItemName = list(self.itemToMod.keys())[0]
        self.ids["CurrencyValue"].text = str(self.itemToMod[ItemName]['Currency'])
        self.ids["PortfolioName"].text = ItemName

    def Confirm(self, App):
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