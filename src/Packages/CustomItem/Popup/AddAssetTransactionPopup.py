from kivy.lang import Builder
from kivy.uix.modalview import ModalView
import Packages.CustomItem.Popup.WarningPopup as Wrn_popup
from kivy.uix.modalview import ModalView
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.CustomItem.Popup.AddFeePopup import AddFeePopup
from Packages.CustomItem.Popup.AddNotePopup import AddNotePopup
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from Packages.CustomFunction.HoverClass import *
from kivy.uix.button import Button
from kivy.properties import ColorProperty
from Packages.CustomItem.DataPicker.CustomDataPickerItem import CustomMDDatePicker
from Packages.CustomItem.Popup.SelectAccountPopup import SelectAccountPopup
import datetime as dt

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddAssetTransactionPopup.kv')

#################
# CUSTOM BUTTON #
#################

class CustomTransactionMenuSquareButton(Button, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
    BackgroundColor = ColorProperty(Configuration.GetElementValue('TransparentBackgroundColor'))
    SelectedStatus = BooleanProperty(False)

    # Function to call to move among different screen
    def move_transaction_screen(self, root):
        # Change current screen
        root.ids['ScreenManagerSection'].current = self.Configuration.GetElementValue('AssetTransactionPopupScreenDictionary')[self.text]

        if self.text == "BUY":
            root.ids.ScreenManagerSection.current_screen.ids.TotalSpentLabel.text = 'Total Spent:'
        elif self.text == "SELL":
            root.ids.ScreenManagerSection.current_screen.ids.TotalSpentLabel.text = 'Total Received:'

        # Update button state
        self.UpdateButtonState(root)

    # Update the button that has been pressed
    def UpdateButtonState(self, root):
        # Update button background button of all buttons
        for element in root.ids['BuySellSwapButtons'].children:
            element.SelectedStatus = False
            element.BackgroundColor = self.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

        self.SelectedStatus = True
        self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 

    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

class CustomDateFeeDateSquareButton(Button, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
    BackgroundColor = ColorProperty(Configuration.GetElementValue('DateFeeNoteBtnNotSelectedBackgroundColor'))
    SelectedStatus = BooleanProperty(False)
    
    ###############
    # DATE PICKER #
    ###############
     
    # Click OK
    def on_save(self, instance, value, date_range):
        self.parent.parent.parent.parent.parent.parent.parent.parent.date = dt.datetime(value.year, value.month, value.day)
        self.parent.parent.parent.parent.parent.ids['DateTextstr'].text = dt.date(value.year, value.month, value.day).strftime("%d %B %Y")
        
    # Show Data Picker
    def show_date_picker(self, date_str):
        date_dialog = CustomMDDatePicker(mode="picker", primary_color= [0.1,0.1,0.9,0.7], selector_color = [0.1,0.1,0.9,0.7], text_button_color = [0.1,0.1,0.9,0.7])
        date_dialog.bind(on_save = self.on_save)
        date_dialog.open()

    ###############
    # FEES PICKER #
    ###############
    def OpeningAddFee(self, fee_str):
        # Define Popup
        Popup = AddFeePopup(fee_str)
        Popup.open()
    
    ###############
    # NOTE PICKER #
    ###############
    def OpeningAddNote(self, note_str):
        # Define Popup
        Popup = AddNotePopup(note_str)
        Popup.open()

    ##########################
    # HOVER BEHAVIOUR PICKER #
    ##########################
    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('DateFeeNoteBtnSelectedBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('DateFeeNoteBtnNotSelectedBackgroundColor') 

###############
# POPUP CLASS #
###############

class AddAssetTransactionPopup(ModalView):
    def __init__(self, title_str = '', type = 'A', AssetName = 'Bitcoin', PortfolioName = '', Database = '', ItemToMod = {}, Currency = '$'): 
        # Setting internal attributes
        self.PortfolioName = PortfolioName
        self.DBManager = Database
        self.title = title_str
        self.Currency = Currency
        self.AssetName = AssetName
        self.SelectedPayingAccount = {}
        self.SelectedStoringAccount = {}
        self.fee = '0.0'
        self.note = ''
        self.date = dt.datetime.now()
        
        # Initialize the super class
        super().__init__(size_hint = (0.33,0.7))

        # Modify BUY button as selected one
        self.ids['BUY_BTN'].SelectedStatus = True
        self.ids['BUY_BTN'].BackgroundColor = self.ids['BUY_BTN'].Configuration.GetElementValue('MenuButtonSelectedBackgroundColor')

        # Set the current date on the button
        self.ids['ScreenManagerSection'].current_screen.ids['DateTextstr'].text = dt.date(self.date.year, self.date.month, self.date.day).strftime("%d %B %Y")

        # Set the asset and symbol according to the page the popup was opened
        self.ids['ScreenManagerSection'].current_screen.ids['PricePerCoinStr'].text = 'Price Per Coin'
        self.ids['ScreenManagerSection'].current_screen.ids['TotalSpentValue'].text = self.Currency + '0.0'

        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        self.ids["Confirm"].text = "Modify Transaction" if type == 'M' else "Add Transaction"

        # Define dropdown list of buttons
        Accounts = ['Unicredit Accounts', 'Ledger' , 'DeGiro']

        # Update Asset Name and Symbol
        self.UpdateAssetNameSymbol()

        # Fill the popup if the user need to modify a field
        if ItemToMod: 
            # Save item to modify
            self.ItemIndex = list(ItemToMod.keys())[0]
            self.itemToMod = ItemToMod[self.ItemIndex]
            self.ModifyTextInput()
      
    ######################
    # INTERNAL FUNCTIONS #
    ######################
    # Function to call Asset Image, Asset Name and Asset Symbol at Popup opening
    def UpdateAssetNameSymbol(self):
        return
        self.ids['AssetName'].text = 'Asset: ' + self.AssetName.upper()
        self.ids['SymbolName'].text = 'Symbol: ' + self.DBManager.ReadJson()[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['Symbol'].upper()

    # Function to call to pre-fill the popup when it is called to modify a transaction
    def ModifyTextInput(self):
        return
        # Update symbol
        self.UpdateAssetNameSymbol()

        # Modify text input if itemToMod is not empty
        self.ids["TypeValue"].text = self.itemToMod['Type']
        self.ids["DateValue"].text = self.itemToMod['Date']
        self.ids["PriceValue"].text = self.itemToMod['Price']
        self.ids["QuantityValue"].text = self.itemToMod['Amount']
    
    #############################
    # OPENING CLOSING FUNCTIONS #
    #############################
    
    # Function to call when the Cancel button is pressed
    def Cancel(self):
        self.dismiss()
    
    # Function to call to add the transaction to portfolio
    def AddTransaction(self, App):
        # Keep the boolean error
        string = ''
        return

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
                self.DBManager.ModifyTransactionToAsset(PortfolioName = self.PortfolioName, AssetName = self.AssetName, ItemIndex = self.ItemIndex, NewTransaction = TransactiontoAdd)
            else:
                self.DBManager.AddTransactionToAsset(self.PortfolioName, self.AssetName, TransactiontoAdd)

            # Update Asset Statistics
            self.DBManager.UpdateAssetStatistics(self.PortfolioName, self.AssetName)
            
            # Update the Json and Update the Dashboard Screen
            ActualScreen = App.root.children[0].children[0].current_screen
            ActualScreen.UpdateScreen(ActualScreen.AssetName, ActualScreen.PortfolioName, ActualScreen.FromScreenName)

            # Close the popup
            self.dismiss()

        print('Adding Transactions...')
        self.dismiss()

class BuySellScreen(Screen):

    def open_select_account_popup(self, title_str, type_str):

        Popup = SelectAccountPopup(title_str = title_str, CurrentAsset = self.parent.parent.parent.AssetName, PortfolioCurrency = self.parent.parent.parent.Currency, type = type_str)
        Popup.open()

    def compute_value_spent(self):
        # Initialize Values
        Quantity = 0.0
        PricePerCoin = 0.0
        skipComputation = 0
        if self.ids['QuantityValue'].text == '' or self.ids['PricePerCoinValue'].text == '': return

        # Extract Quantity 
        if ('%s' % self.ids['QuantityValue'].text).replace('.','').replace(',','').isnumeric():
            # Check correctness
            Quantity = self.ids['QuantityValue'].text.replace(',','.')

            counter = Quantity.count('.')
            while counter > 1:
                Quantity = Quantity.replace('.','',1)
                counter = Quantity.count('.')
                self.ids['QuantityValue'].text = Quantity
    
            Quantity = float(Quantity)
        else:
            self.ids['QuantityValue'].text = '0.0'
            skipComputation = 1

        # Extract Prince Per Coint
        if ('%s' % self.ids['PricePerCoinValue'].text).replace('.','').replace(',','').isnumeric():
            PricePerCoin = self.ids['PricePerCoinValue'].text.replace(',','.')

            counter = PricePerCoin.count('.')
            while counter > 1:
                PricePerCoin = PricePerCoin.replace('.','',1)
                counter = PricePerCoin.count('.')
                self.ids['PricePerCoinValue'].text = PricePerCoin
            PricePerCoin = float(PricePerCoin)
        else:
            self.ids['PricePerCoinValue'].text = '0.0' + self.parent.parent.parent.Currency
            skipComputation = 1

        # Compute 
        if skipComputation: return
    
        self.ids['TotalSpentValue'].text = self.parent.parent.parent.Currency + str(round((Quantity * PricePerCoin), 5)) 

class SwapScreen(Screen):
    pass

