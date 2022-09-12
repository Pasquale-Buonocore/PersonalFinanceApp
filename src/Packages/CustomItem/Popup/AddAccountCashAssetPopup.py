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
from kivy.properties import ColorProperty
from kivymd.app import MDApp

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddAccountCashAssetPopup.kv')

class AddAccountCashAssetPopup(ModalView):
    def __init__(self, AccountName, cash_or_asset = 'cash'):
        # # Define popup internal signals according to cash or asset
        # - Change title
        self.cash_or_asset = cash_or_asset
        self.AccountName = AccountName
        self.title = 'ADD ' + cash_or_asset.upper()

        # - Change confirmation button string
        self.confirm_btn_str = 'Add ' + cash_or_asset + ' item'

        # - Enable Based On currency box layout
        self.BoxLayoutOpacity = 1
        
        # Disable the Based On Currency item
        if cash_or_asset == 'asset': self.BoxLayoutOpacity = 0

        # Initialize the super class
        super().__init__(size_hint = (0.25,0.5))

        
    def AddItem(self):
        # Keep the boolean error
        string = ''

        # Retrive data "Account Name" from Text Input - In empty do nothing
        CurrencyNameValue = self.ids["CurrencyNameValue"].text.strip()
        if not CurrencyNameValue: string = string + 'ERROR: Empty Currency Name FIELD'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + '\nERROR: Empty Symbol value FIELD'
        
        # Retrive data "Based On Currency Value" from Text Input - In empty do nothing
        BasedOnCurrencyValue = self.ids["BasedOnCurrencyValue"].text.strip()
        if self.cash_or_asset == 'cash' and (not BasedOnCurrencyValue): string = string + '\nERROR: Empty Based On Currency value FIELD'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
            return

        # Define Asset To Add in <self.portfolio> portfolio
        if self.cash_or_asset == 'cash': 
            MDApp.get_running_app().Accounts_DB.AddCashSubAccountCategory(AccountName = self.AccountName,
                                                                          CashCategory = CurrencyNameValue,
                                                                          Symbol = SymbolValue,
                                                                          BasedCarrency = BasedOnCurrencyValue)
                                                                          
        if self.cash_or_asset == 'asset': 
            MDApp.get_running_app().Accounts_DB.AddAssetSubAccountCategory(AccountName = self.AccountName,
                                                                           AssetCategory = CurrencyNameValue,
                                                                           Symbol = SymbolValue)

        # Then Update Screen
        MDApp.get_running_app().root.children[0].children[0].current_screen.UpdateScreen()

        # Close the popup
        self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()