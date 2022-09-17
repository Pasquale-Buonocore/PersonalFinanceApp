from kivy.lang import Builder
from kivy.uix.popup import Popup
import Packages.CustomItem.Popup.WarningPopup as Wrn_popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddAssetPopup.kv')

class AddAssetPopup(Popup):
    def __init__(self, title_str, type, Database, PortfolioName,  itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint = (0.3,0.5))
        self.PortfolioName = PortfolioName
        self.DBManager = Database

        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        ItemName = list(self.itemToMod.keys())[0]
        self.ids["SymbolValue"].text = str(self.itemToMod[ItemName]['Symbol'])
        self.ids["AssetName"].text = ItemName

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Asset Name" from Text Input - In empty do nothing
        AssetName = self.ids["AssetName"].text.strip().title()
        if not AssetName: string = string + 'ERROR: Empty asset name FIELD'

        # Retrive data "Currency Value" from Text Input - In empty do nothing
        CurrencySymbol = self.ids["SymbolValue"].text.strip().upper()
        if not CurrencySymbol: string = string + '\nERROR: Empty symbol value FIELD'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
        else:

            # Define Asset To Add
            AssetToAdd = self.DBManager.InitializeNewAsset(AssetName, CurrencySymbol)
            
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                self.DBManager.ModifyAssetInPortfolio(self.PortfolioName, list(self.itemToMod.keys())[0], AssetName, CurrencySymbol)
            else:
                # Check if the Portfolio already exists
                AssetAlreadyPresent = list(self.DBManager.ReadJson()[self.PortfolioName]['Assets'].keys())
                if AssetName in AssetAlreadyPresent:
                    # Show a warning message
                    string = 'The asset ' + AssetName + ' already exists.\n It cannot be added. Remove it first!'
                    Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
                    Pop.open()
                else:
                    # Append new item
                    self.DBManager.AddAssetToPortfolio(self.PortfolioName, AssetToAdd)

            # Update the Json and Update the Dashboard Screen
            ActualScreen = App.root.children[0].children[0].current_screen
            ActualScreen.UpdateScreen(ActualScreen.FromScreenName, ActualScreen.PortfolioName, ActualScreen.PortfolioCurrency)

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()