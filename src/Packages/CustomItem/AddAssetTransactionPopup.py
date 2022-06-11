from kivy.lang import Builder
from kivy.uix.popup import Popup
import Packages.CustomItem.WarningPopup as Wrn_popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddAssetTransactionPopup.kv')

class AddAssetTransactionPopup(Popup):
    def __init__(self, title_str, type = 'A', AssetName = '', PortfolioName = '', Database = '', ItemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint = (0.4,0.6))
        # Save important infos
        self.DBManager = Database
        self.PortfolioName = PortfolioName
        self.AssetName = AssetName
        self.Note = '' # It will in future filled with a note writtable by the user
        self.Fees = 0 # It will in future filled with a value by the user

        # Update Asset Name and Symbol
        self.UpdateAssetNameSymbol()

        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
       
        # Fill the popup if the user need to modify a field
        if ItemToMod: 
            # Save item to modify
            self.ItemIndex = list(ItemToMod.keys())[0]
            self.itemToMod = ItemToMod[self.ItemIndex]
            self.ModifyTextInput()

    def UpdateAssetNameSymbol(self):
        self.ids['AssetName'].text = 'Asset: ' + self.AssetName.upper()
        self.ids['SymbolName'].text = 'Symbol: ' + self.DBManager.ReadJson()[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['Symbol'].upper()

    def ModifyTextInput(self):
        # Update symbol
        self.UpdateAssetNameSymbol()

        # Modify text input if itemToMod is not empty
        self.ids["TypeValue"].text = self.itemToMod['Type']
        self.ids["DateValue"].text = self.itemToMod['Date']
        self.ids["PriceValue"].text = self.itemToMod['Price']
        self.ids["QuantityValue"].text = self.itemToMod['Amount']

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Type Name" from Text Input - In empty do nothing
        TypeValue = self.ids["TypeValue"].text.strip().upper()
        if not TypeValue: string = string + 'ERROR: Empty type value FIELD'

        # Retrive data "Date Value" from Text Input - In empty do nothing
        DateValue = self.ids["DateValue"].text.strip().upper()
        if not DateValue: string = string + '\nERROR: Empty date value FIELD'

        # Retrive data "Price Value" from Text Input - In empty do nothing
        PriceValue = self.ids["PriceValue"].text.strip().upper()
        if not PriceValue: string = string + '\nERROR: Empty price value FIELD'

        # Retrive data "Quantity Value" from Text Input - In empty do nothing
        QuantityValue = self.ids["QuantityValue"].text.strip().upper()
        if not QuantityValue: string = string + '\nERROR: Empty quantity value FIELD'

        FeesValue = self.Fees
        NoteValue = self.Note

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
        else:
            # Define Asset To Add
            TransactiontoAdd = self.DBManager.InitializeTransaction(TypeValue, DateValue, PriceValue, QuantityValue, FeesValue, NoteValue)

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                self.DBManager.ModifyAssetInPortfolio(self.PortfolioName, list(self.itemToMod.keys())[0], AssetName, CurrencySymbol)
            else:
                self.DBManager.AddTransactionToAsset(self.PortfolioName, self.AssetName, TransactiontoAdd)

            # Update the Json and Update the Dashboard Screen
            ActualScreen = App.root.children[0].children[0].current_screen
            ActualScreen.UpdateScreen(ActualScreen.AssetName, ActualScreen.PortfolioName, ActualScreen.FromScreenName)

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()