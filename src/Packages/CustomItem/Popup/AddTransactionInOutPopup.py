from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
import Packages.CustomItem.Popup.WarningPopup as Wrn_popup 
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
import datetime as dt
from Packages.CustomFunction.HoverClass import *
from kivy.uix.button import Button
from Packages.CustomFunction.CustomFunction import verify_numeric_float_string
from Packages.CustomItem.DataPicker.CustomDataPickerItem import CustomMDDatePicker
from Packages.CustomItem.Popup.SelectAccountPopup import SelectAccountPopupTransaction
from Packages.CustomItem.Popup.SelectTransactionCategory import SelectTransactionCategory
from Packages.CustomFunction.GenerateTransactionLinkingCode import generate_transaction_linking_code
from Packages.CustomFunction.CustomFunction import check_if_balance_is_not_enough
from kivy.properties import ColorProperty
from kivymd.app import MDApp

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddTransactionInOutPopup.kv')

class CustomeDateSquareButton(Button, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)
    BackgroundColor = ColorProperty(Configuration.GetElementValue('WindowBackgroundColor'))
    SelectedStatus = BooleanProperty(False)
    
    ###############
    # DATE PICKER #
    ###############
     
    # Click OK
    def on_save(self, instance, value, date_range):
        self.parent.parent.parent.parent.parent.parent.parent.date = dt.datetime(value.year, value.month, value.day)
        self.parent.parent.parent.parent.parent.parent.parent.ids['DateTextstr'].text = dt.date(value.year, value.month, value.day).strftime("%d %B %Y")
        
    # Show Data Picker
    def show_date_picker(self, date_str):
        date_dialog = CustomMDDatePicker(mode="picker", primary_color= self.Configuration.GetElementValue('WindowBackgroundColor') , selector_color = [0.1,0.1,0.9,0.7], text_button_color = [0.1,0.1,0.9,0.7])
        date_dialog.bind(on_save = self.on_save)
        date_dialog.open()

    ##########################
    # HOVER BEHAVIOUR PICKER #
    ##########################
    
    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('LightCanvasBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('WindowBackgroundColor') 

class AddTransactionInOutPopup(ModalView):
    def __init__(self, title_str = '', type = 'A', PortfolioName = '', Database = '', ItemToMod = {}):
        # Define popup internal signals
        self.title = title_str
        self.SelectedPayingAccount = {}
        self.SelectedCategory = ''
        self.DBManager = Database
        self.note = ''
        self.date = dt.datetime.now()
        self.Amount = '0.0'
        self.PortfolioName = PortfolioName if PortfolioName in ['IN', 'OUT'] else 'IN'

        self.AvailableCategory = list(self.DBManager.ReadJson()[self.PortfolioName]['Assets'].keys()) + ['Internal Transaction']
        if self.PortfolioName == 'IN': self.AvailableCategory += ['Account Initialization']

        self.Linking_code_first_char = 'E' if self.PortfolioName == 'IN' else 'S'

        # Initialize the super class
        super().__init__(size_hint = (0.3,0.6))
        
        # Set the current date on the button
        self.ids['DateTextstr'].text = dt.date(self.date.year, self.date.month, self.date.day).strftime("%d %B %Y")

        # Set the first category of the transactions
        self.ids.CategoryValue.text = self.AvailableCategory[0] if self.AvailableCategory else '---'
        
        self.ids.PayingWithLabel.text = 'Earning Account' if (self.PortfolioName == 'IN') else 'Paying Account'

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

    def open_select_category_popup(self):
        Popup = SelectTransactionCategory(AvailableCategory = self.AvailableCategory)
        Popup.open()

    def open_select_account_popup(self):
        # Define popup and open it
        title_str = 'SELECT PAYING ACCOUNT' if self.PortfolioName == 'OUT' else 'SELECT EARNING ACCOUNT'
        type_str = 'expense' if self.PortfolioName == 'OUT' else 'earning'

        Popup = SelectAccountPopupTransaction(title_str = title_str, type_str = type_str)
        Popup.open()

    def CheckQuantityValue(self):
        # Check correctness
        Quantity = verify_numeric_float_string(self.ids['QuantityValue'].text)

        # Update string in GUI
        self.ids['QuantityValue'].text = Quantity
        
    def AddTransaction(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Type Name" from Text Input - In empty do nothing
        CategoryValue = self.ids["CategoryValue"].text.strip()
        if not CategoryValue: string = string + 'ERROR: Empty category value FIELD'

        # Retrive data "Date Value" from Text Input - In empty do nothing
        DateValue = self.ids["DateTextstr"].text.strip().upper()
        if not DateValue: string = string + '\nERROR: Empty date value FIELD'

        # Retrive data "Amount Value" from Text Input - In empty do nothing
        AmountValue = self.ids["QuantityValue"].text.strip()
        if not AmountValue: string = string + '\nERROR: Empty amount value FIELD'

        # Retrive data "Quantity Value" from Text Input - In empty do nothing
        PaidWithValue = self.ids["PayingAccountString"].text.strip()
        if not PaidWithValue: string = string + '\nERROR: Empty PaidWith value FIELD'

        # Retrive data "Note Value" from Text Input - In empty do nothing
        NoteValue = self.ids["DescriptionValue"].text.strip().upper()

        # Define the currency with is the symbol of the value selected as paying account
        # Currency = MDApp.get_running_app().Accounts_DB.ReadJson()[self.SelectedPayingAccount['Account']]['SubAccount'][self.SelectedPayingAccount['SubAccount']][self.SelectedPayingAccount['Currency']]['Symbol']
        Currency = self.SelectedPayingAccount['Currency']

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
            return

        # Before adding the transaction, in case of spending transaction, if the balance is enough
        Paying_account_available_balance = MDApp.get_running_app().Accounts_DB.ReadJson()[self.SelectedPayingAccount['Account']]['SubAccount'][self.SelectedPayingAccount['SubAccount']][self.SelectedPayingAccount['Currency']]['LiquidityContribution']
        if self.PortfolioName == 'OUT' and check_if_balance_is_not_enough(available_amount = Paying_account_available_balance, transaction_amount = AmountValue):
            # If the error message is not empty, display an error
            message = 'Available balance is not enough. \n Transaction cannot be added'
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', message)
            Pop.open()
            return

        # Define Asset To Add in <self.portfolio> portfolio
        TransactiontoAdd = self.DBManager.InitializeNewTransactionInOut(DateValue, round(float(AmountValue),2), Currency, CategoryValue, PaidWithValue, NoteValue)
        
        # If an item needs to be modified
        if self.type == 'M':
            # Substitute the actual item
            self.DBManager.ModifyTransactionToAsset(PortfolioName = self.PortfolioName, AssetName = CategoryValue, ItemIndex = self.ItemIndex, NewTransaction = TransactiontoAdd)
        else:

            # Add transaction to Account database
            Result = 1
            while Result:
                # Generate a code to link the transaction among Account and Transaction Json
                LinkingCode = generate_transaction_linking_code(first_char = self.Linking_code_first_char, second_char = 'S')

                # Try to add the transaction until a random number is picked
                Result = MDApp.get_running_app().Accounts_DB.AppendTransactionToList(AccountName = self.SelectedPayingAccount['Account'],
                                                                                        cash_or_asset = self.SelectedPayingAccount['SubAccount'],
                                                                                        AssetName = self.SelectedPayingAccount['Currency'],
                                                                                        TransactionToAppendDict = {LinkingCode : TransactiontoAdd})

            # Add transaction to Transaction List
            TransactiontoAdd.update({'LinkingCode' : LinkingCode})
            self.DBManager.AddTransactionToAsset(self.PortfolioName, CategoryValue, TransactiontoAdd)
            self.DBManager.AddTransactionToAsset(self.PortfolioName + '_LIST', "Transactions", TransactiontoAdd)

        # Update Paying Account statistics
        MDApp.get_running_app().Accounts_DB.Update_liquid_investing_balance(self.SelectedPayingAccount['Account'], self.SelectedPayingAccount['SubAccount'], self.SelectedPayingAccount['Currency'])

        # Update Asset Statistics in transaction list
        self.DBManager.UpdateAssetInTransactionStatistics(self.PortfolioName, CategoryValue)
        
        # Update the Json and Update the Dashboard Screen
        ActualScreen = App.root.children[0].children[0].current_screen
        ActualScreen.UpdateScreen(self.PortfolioName, self.DBManager)

        # Close the popup
        self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()