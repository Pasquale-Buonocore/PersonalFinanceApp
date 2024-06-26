from kivy.uix.modalview import ModalView
import Packages.CustomItem.Popup.WarningPopup as Wrn_popup
from kivy.uix.modalview import ModalView
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.CustomItem.Popup.AddFeePopup import AddFeePopup
from Packages.CustomItem.Popup.AddNotePopup import AddNotePopup
from Packages.CustomFunction.CustomFunction import verify_numeric_float_string
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from Packages.CustomFunction.HoverClass import *
from kivy.uix.button import Button
from kivy.properties import ColorProperty
from Packages.CustomItem.DataPicker.CustomDataPickerItem import CustomMDDatePicker
from Packages.CustomItem.Popup.SelectAccountPopup import SelectAccountPopup, SelectAccountPopupInvestment
import datetime as dt
from kivymd.app import MDApp
from Packages.CustomFunction.GenerateTransactionLinkingCode import generate_transaction_linking_code
from Packages.CustomFunction.CustomFunction import check_if_balance_is_not_enough

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddAssetTransactionPopup.kv')

#################
# CUSTOM BUTTON #
#################

class CustomTransactionMenuSquareButton(Button, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)
    BackgroundColor = ColorProperty(Configuration.GetElementValue('TransparentBackgroundColor'))
    SelectedStatus = BooleanProperty(False)

    # Function to call to move among different screen
    def move_transaction_screen(self, root):
        # Change current screen
        root.ids['ScreenManagerSection'].current = self.Configuration.GetElementValue('AssetTransactionPopupScreenDictionary')[self.text]

        if self.text == "BUY":
            root.ids.ScreenManagerSection.current_screen.ids.TotalSpentLabel.text = 'Total Spent:'
            root.ids.ScreenManagerSection.current_screen.ids.SwitchValue.active = False
            root.ids.ScreenManagerSection.current_screen.ids.SwitchValue.disabled = True
        elif self.text == "SELL":
            root.ids.ScreenManagerSection.current_screen.ids.TotalSpentLabel.text = 'Total Received:'
            root.ids.ScreenManagerSection.current_screen.ids.SwitchValue.active = False
            root.ids.ScreenManagerSection.current_screen.ids.SwitchValue.disabled = False

        # Update button state
        self.UpdateButtonState(root)

    # Update the button that has been pressed
    def UpdateButtonState(self, root):
        # Update button background button of all buttons
        for element in root.ids['BuySellSwapButtons'].children:
            element.SelectedStatus = False 
            element.BackgroundColor = self.Configuration.GetElementValue('CanvasBackgroundColor') 

        self.SelectedStatus = True
        self.BackgroundColor = self.Configuration.GetElementValue('WindowBackgroundColor') 

    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('WindowBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('CanvasBackgroundColor') 

class CustomDateFeeDateSquareButton(Button, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)
    BackgroundColor = ColorProperty(Configuration.GetElementValue('WindowBackgroundColor'))
    SelectedStatus = BooleanProperty(False)
    
    ###############
    # DATE PICKER #
    ###############
     
    # Click OK
    def on_save(self, instance, value, date_range):
        self.parent.parent.parent.parent.parent.parent.parent.parent.parent.date = dt.datetime(value.year, value.month, value.day)
        self.parent.parent.parent.parent.parent.ids['DateTextstr'].text = dt.date(value.year, value.month, value.day).strftime("%d %B %Y")
        
    # Show Data Picker
    def show_date_picker(self, date_str):
        date_dialog = CustomMDDatePicker(mode="picker", primary_color= self.Configuration.GetElementValue('WindowBackgroundColor') , selector_color = [0.1,0.1,0.9,0.7], text_button_color = [0.1,0.1,0.9,0.7])
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
        self.BackgroundColor = self.Configuration.GetElementValue('LightCanvasBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('WindowBackgroundColor') 

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
        super().__init__(size_hint = (0.33,0.75))

        # Modify BUY button as selected one
        self.ids['BUY_BTN'].SelectedStatus = True
        self.ids['BUY_BTN'].BackgroundColor = self.ids['BUY_BTN'].Configuration.GetElementValue('WindowBackgroundColor')

        # Set the Asset and Symbol to transact
        self.ids['ScreenManagerSection'].current_screen.ids['AssetSymbolstr'].text = self.AssetName

        # Set the current date on the button
        self.ids['ScreenManagerSection'].current_screen.ids['DateTextstr'].text = dt.date(self.date.year, self.date.month, self.date.day).strftime("%d %B %Y")
        
        # Set the asset and symbol according to the page the popup was opened
        self.ids['ScreenManagerSection'].current_screen.ids['PricePerCoinStr'].text = 'Price Per Coin'
        self.ids['ScreenManagerSection'].current_screen.ids['TotalSpentValue'].text = self.Currency + '0.0'

        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        self.ids["Confirm"].text = "Modify Transaction" if type == 'M' else "Add Transaction"

        # Define dropdown list of buttons
        # Accounts_dict = MDApp.get_running_app().Accounts_DB.ReadJson()

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

        # Retrive data "Type Name" from Text Input - In empty do nothing
        TypeValue = ''
        if self.ids.SELL_BTN.SelectedStatus:  TypeValue = 'SELL'
        if self.ids.BUY_BTN.SelectedStatus:  TypeValue = 'BUY'
        if not TypeValue: string = string + 'ERROR: Empty type value FIELD'

        # Retrive data "Price Value" from Text Input - In empty do nothing
        PriceValue = self.ids['ScreenManagerSection'].current_screen.ids.PricePerCoinValue.text
        if not PriceValue: string = string + '\nERROR: Empty price value FIELD'

        # Retrive data "Quantity Value" from Text Input - In empty do nothing
        QuantityValue = self.ids['ScreenManagerSection'].current_screen.ids.QuantityValue.text
        if not QuantityValue: string = string + '\nERROR: Empty quantity value FIELD'

        # Retrieve total spent value
        TotalSpentValue = float(QuantityValue) * float(PriceValue)

        FeesValue = self.fee
        if not FeesValue: string = string + '\nERROR: Empty fee value FIELD'

        NoteValue = self.note

        # Retrive data "Date Value" from Text Input - In empty do nothing
        DateValue = self.ids['ScreenManagerSection'].current_screen.ids.DateTextstr.text
        if not DateValue: string = string + '\nERROR: Empty date value FIELD'

        # Paying Account
        if not self.SelectedPayingAccount: string = string + '\nERROR: Empty Paying Account value FIELD'
        
        if not self.SelectedStoringAccount: string = string + '\nERROR: Empty Storing Account value FIELD'
            

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
            return
            
        if not (TypeValue == 'SELL'):

            # Define Asset To Add
            TransactiontoAdd = self.DBManager.InitializeTransaction(DateValue, PriceValue, QuantityValue, FeesValue, NoteValue, self.SelectedPayingAccount, self.SelectedStoringAccount)
            
            
            PortfolioAccountString = {'json_file' : self.DBManager.json_path}
            PortfolioAccountString.update({'PortfolioName': self.PortfolioName})
            PortfolioAccountString.update({'AssetName': self.AssetName})
            
            # Define Transaction to add to paying account
            TransactiontoAddPayingAccount = MDApp.get_running_app().Accounts_DB.Initialize_investiment_transaction_to_store_into_account(DateValue, 
                                                                                                                                         round(float(TotalSpentValue),3),
                                                                                                                                         'Paying investment',
                                                                                                                                         PortfolioAccountString,
                                                                                                                                         NoteValue)
            
            # Define Transaction to add to storing account
            TransactiontoAddStoringAccount = MDApp.get_running_app().Accounts_DB.Initialize_investiment_transaction_to_store_into_account(DateValue,
                                                                                                                                          round(float(QuantityValue),5),
                                                                                                                                          'Storing investment',
                                                                                                                                          PortfolioAccountString,
                                                                                                                                          NoteValue)
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                self.DBManager.ModifyTransactionToAsset(PortfolioName = self.PortfolioName, AssetName = self.AssetName, ItemIndex = self.ItemIndex, NewTransaction = TransactiontoAdd)
            else:
                
                # Before adding the transaction, in case of spending transaction, if the balance is enough
                Paying_account_available_balance = MDApp.get_running_app().Accounts_DB.ReadJson()[self.SelectedPayingAccount['Account']]['SubAccount'][self.SelectedPayingAccount['SubAccount']][self.SelectedPayingAccount['Currency']]['LiquidityContribution']
                if check_if_balance_is_not_enough(available_amount = Paying_account_available_balance, transaction_amount = TotalSpentValue):
                    # If the error message is not empty, display an error
                    message = 'Available balance is not enough. \n Transaction cannot be added'
                    Pop = Wrn_popup.WarningPopup('WARNING WINDOW', message)
                    Pop.open()
                    return

                ##########################
                #  Update Paying account #
                ##########################
                Result = 1

                while Result:
                    # Generate a code to link the transaction among Account and Transaction Json
                    LinkingCode = generate_transaction_linking_code(first_char = 'O', second_char = 'I')

                    # Try to add the transaction until a random number is picked
                    Result = MDApp.get_running_app().Accounts_DB.AppendTransactionToList(AccountName = self.SelectedPayingAccount['Account'],
                                                                                        cash_or_asset = self.SelectedPayingAccount['SubAccount'],
                                                                                        AssetName = self.SelectedPayingAccount['Currency'],
                                                                                        TransactionToAppendDict = {LinkingCode : TransactiontoAddPayingAccount})
                TransactiontoAdd.update({'PayingAccountLinkingCode' : LinkingCode})

                ###########################
                #  Update Storing account #
                ###########################
                Result = 1

                while Result:
                    # Generate a code to link the transaction among Account and Transaction Json
                    LinkingCode = generate_transaction_linking_code(first_char = 'S', second_char = 'I')

                    # Try to add the transaction until a random number is picked
                    Result = MDApp.get_running_app().Accounts_DB.AppendTransactionToList(AccountName = self.SelectedStoringAccount['Account'],
                                                                                        cash_or_asset = self.SelectedStoringAccount['SubAccount'],
                                                                                        AssetName = self.SelectedStoringAccount['Currency'],
                                                                                        TransactionToAppendDict = {LinkingCode : TransactiontoAddStoringAccount})
                TransactiontoAdd.update({'StoringAccountLinkingCode' : LinkingCode})

                ##########################################
                #  Update investment transaction account #
                ##########################################
                
                self.DBManager.AddTransactionToAsset(self.PortfolioName, self.AssetName, TransactiontoAdd)

            # Update Asset Statistics
            self.DBManager.UpdateAssetStatistics(self.PortfolioName, self.AssetName)

            # Update Paying Account statistics
            MDApp.get_running_app().Accounts_DB.Update_liquid_investing_balance(self.SelectedPayingAccount['Account'], self.SelectedPayingAccount['SubAccount'], self.SelectedPayingAccount['Currency'])

            # Update Storing Account statistics
            MDApp.get_running_app().Accounts_DB.Update_liquid_investing_balance(self.SelectedStoringAccount['Account'], self.SelectedStoringAccount['SubAccount'], self.SelectedStoringAccount['Currency'])

            # Update the Json and Update the Dashboard Screen
            ActualScreen = App.root.children[0].children[0].current_screen
            ActualScreen.UpdateScreen(ActualScreen.AssetName, ActualScreen.PortfolioName, self.Currency, ActualScreen.FromScreenName)

        else:
            self.paying_account_char = 'CI'
            self.storing_account_Char = 'DI'
            
        # Close the popup
        self.dismiss()

        print('Adding Transactions...')

class BuySellScreen(Screen):

    def open_select_account_popup(self, title_str, type_str):
        Popup = SelectAccountPopupInvestment(title_str = title_str, CurrentAsset = self.parent.parent.parent.parent.AssetName, PortfolioCurrency = self.parent.parent.parent.parent.Currency, type = type_str)
        Popup.open()

    def compute_value_spent(self):
        # Initialize Values
        Quantity = 0.0
        PricePerCoin = 0.0
        skipComputation = 0
        if self.ids['QuantityValue'].text == '' or self.ids['PricePerCoinValue'].text == '': return

        ####################
        # Extract Quantity #
        ####################
        # Check correctness
        Quantity = verify_numeric_float_string(self.ids['QuantityValue'].text)

        # Update string in GUI
        self.ids['QuantityValue'].text = Quantity

        # Convert into float
        Quantity = float(Quantity) if Quantity else float('0.0')

        ##########################
        # Extract Price Per Coin #
        ##########################
        # Check correctness
        PricePerCoin = verify_numeric_float_string(self.ids['PricePerCoinValue'].text)

        # Update string in GUI
        self.ids['PricePerCoinValue'].text = PricePerCoin

        # Convert into float
        PricePerCoin = float(PricePerCoin) if PricePerCoin else float('0.0')
    
        self.ids['TotalSpentValue'].text = self.parent.parent.parent.parent.Currency + str(round((Quantity * PricePerCoin), 5)) 

class SwapScreen(Screen):
    pass

