from kivy.lang import Builder
from kivy.uix.popup import Popup
import Packages.CustomItem.WarningPopup as Wrn_popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddTransactionInOutPopup.kv')

class AddTransactionInOutPopup(Popup):
    def __init__(self, title_str = '', type = 'A', PortfolioName = '', Database = '', ItemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint = (0.4,0.6))
        # Save important infos
        self.DBManager = Database

        # Define inner attributes - direction
        self.PortfolioName = PortfolioName if PortfolioName in ['IN', 'OUT'] else 'IN'

        # Define inner attributes - type
        self.type = type if type in ['A','M'] else 'A'
        self.ids["Confirm"].text = "Modify Transaction" if type == 'M' else "Add Transaction"

        # Fill the popup if the user need to modify a field
        if ItemToMod: 
            # Save item to modify
            self.ItemIndex = list(ItemToMod.keys())[0]
            self.itemToMod = ItemToMod[self.ItemIndex]
            self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        self.ids["CategoryValue"].text = self.itemToMod['Category']
        self.ids["DateValue"].text = self.itemToMod['Date']
        self.ids["AmountValue"].text = str(self.itemToMod['Amount'])
        self.ids["PaidWithValue"].text = self.itemToMod['Paid with']
        self.ids["NoteValue"].text = self.itemToMod['Note']


    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Type Name" from Text Input - In empty do nothing
        CategoryValue = self.ids["CategoryValue"].text.strip()
        if not CategoryValue: string = string + 'ERROR: Empty category value FIELD'

        # Retrive data "Date Value" from Text Input - In empty do nothing
        DateValue = self.ids["DateValue"].text.strip().upper()
        if not DateValue: string = string + '\nERROR: Empty date value FIELD'

        # Retrive data "Amount Value" from Text Input - In empty do nothing
        AmountValue = self.ids["AmountValue"].text.strip().upper()
        if not AmountValue: string = string + '\nERROR: Empty amount value FIELD'

        # Retrive data "Quantity Value" from Text Input - In empty do nothing
        PaidWithValue = self.ids["PaidWithValue"].text.strip().upper()
        if not PaidWithValue: string = string + '\nERROR: Empty PaidWith value FIELD'

        # Retrive data "Note Value" from Text Input - In empty do nothing
        NoteValue = self.ids["NoteValue"].text.strip().upper()
        if not NoteValue: string = string + '\nERROR: Empty note value FIELD'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
        else:
            # Define Asset To Add
            TransactiontoAdd = self.DBManager.InitializeNewTransactionInOut([DateValue, round(float(AmountValue),2), '€', CategoryValue, PaidWithValue, NoteValue])

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                self.DBManager.ModifyTransactionToAsset(PortfolioName = self.PortfolioName, AssetName = CategoryValue, ItemIndex = self.ItemIndex, NewTransaction = TransactiontoAdd)
            else:
                self.DBManager.AddTransactionToAsset(self.PortfolioName, CategoryValue, TransactiontoAdd)

            # Update Asset Statistics
            self.DBManager.UpdateAssetInTransactionStatistics(self.PortfolioName, CategoryValue)
            
            # Update the Json and Update the Dashboard Screen
            ActualScreen = App.root.children[0].children[0].current_screen
            ActualScreen.UpdateScreen(self.PortfolioName, self.DBManager)

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()