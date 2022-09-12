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
Builder.load_file('Packages/CustomItem/ui/AddAccountPopup.kv')

class AddAccountPopup(ModalView):
    def __init__(self, title_str = ''):
        # Define popup internal signals
        self.title = title_str
        self.SelectedCategory = ''
        self.AvailableCategory = MDApp.get_running_app().Configuration_DB.GetElementValue('AccountAvailableCategory')
        # Initialize the super class
        super().__init__(size_hint = (0.25,0.5))
        
        # Set the first category of the transactions
        self.ids.CategoryValue.text = self.AvailableCategory[0] if self.AvailableCategory else '---'

    def open_select_category_popup(self):
        Popup = SelectTransactionCategory(AvailableCategory = self.AvailableCategory)
        Popup.open()
        
    def AddAccount(self):
        # Keep the boolean error
        string = ''

        # Retrive data "Account Name" from Text Input - In empty do nothing
        CategoryValue = self.ids["CategoryValue"].text.strip()
        if not CategoryValue: string = string + 'ERROR: Empty category value FIELD'

        # Retrive data "Account Value" from Text Input - In empty do nothing
        AccountValue = self.ids["AccountValue"].text.strip()
        if not AccountValue: string = string + '\nERROR: Empty account value FIELD'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
            return

        # Define Asset To Add in <self.portfolio> portfolio
        AccountToAdd =  MDApp.get_running_app().Accounts_DB.InitializeNewAccount(AccountName = AccountValue, Category = CategoryValue)
        MDApp.get_running_app().Accounts_DB.AddAccount(AccountToAdd)

        # Then Update Screen
        MDApp.get_running_app().root.children[0].children[0].current_screen.UpdateScreen()

        # Close the popup
        self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()