import kivy
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from numpy import asscalar
from kivy.uix.modalview import ModalView
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.CustomItem.AddFeePopup import AddFeePopup
from Packages.CustomItem.AddNotePopup import AddNotePopup
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from Packages.CustomItem.HoverClass import *
from kivy.uix.button import Button
from kivy.properties import ColorProperty
from Packages.CustomItem.CustomDropDown import CustomDropDown
from Packages.CustomItem.DataPickerItem import MDDatePicker
import datetime as dt

# Designate Out .kv design file
Builder.load_file('popup_test.kv')

class Widgets(Widget):
    def btn(self):
        show_popup()

class P(FloatLayout):
    pass

class MyApp(MDApp):
    def build(self):
        Window.maximize()
        # Define the App configuration Database
        self.Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
        return Widgets()

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
        date_dialog = MDDatePicker(mode="picker", primary_color= [0.1,0.1,0.9,0.7], selector_color = [0.1,0.1,0.9,0.7], text_button_color = [0.1,0.1,0.9,0.7])
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

    ###############
    # HOVER BEHAVIOUR PICKER #
    ###############
    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('DateFeeNoteBtnSelectedBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('DateFeeNoteBtnNotSelectedBackgroundColor') 

class AddAssetTransactionPopup(ModalView):
    def __init__(self, title_str = '', Currency = '$'): 
        # Setting internal attributes
        self.title = title_str
        self.Currency = Currency
        self.fee = '0.0'
        self.note = ''
        self.date = dt.datetime.now()
        
        # Initialize the super class
        super().__init__(size_hint = (0.35,0.7))

        # Modify BUY button as selected one
        self.ids['BUY_BTN'].SelectedStatus = True
        self.ids['BUY_BTN'].BackgroundColor = self.ids['BUY_BTN'].Configuration.GetElementValue('MenuButtonSelectedBackgroundColor')

        # Set the current date on the button
        self.ids['ScreenManagerSection'].current_screen.ids['DateTextstr'].text = dt.date(self.date.year, self.date.month, self.date.day).strftime("%d %B %Y")

        # Set the asset and symbol according to the page the popup was opened
        self.ids['ScreenManagerSection'].current_screen.ids['AssetValue'].text = 'Bitcoin'
        self.ids['ScreenManagerSection'].current_screen.ids['SymbolValue'].text = 'BTC'
        self.ids['ScreenManagerSection'].current_screen.ids['PricePerCoinStr'].text = 'Price Per Coin [' + self.Currency + ']'

        Accounts = ['Unicredit Accounts', 'Ledger' , 'DeGiro']
        # Populate the DropDown PayingWith selection
        self.ids['ScreenManagerSection'].current_screen.ids['PayingAccountBoxLayout'].add_widget(CustomDropDown(ListOfButtons = Accounts).ReturnDropDownButton())
        # Populate the DropDown Storing selection

        # add_widget(CustomDropDown(ListOfButtons = Accounts).ReturnDropDownButton())

    # Function to call when the Cancel button is pressed
    def Cancel(self):
        self.dismiss()
    
    # Function to call to add the transaction to portfolio
    def AddTransaction(self, DBManager):
        print('Adding Transactions...')
        self.dismiss()

class BuySellScreen(Screen):

    def compute_value_spent(self):
        # Initialize Values
        Quantity = 0.0
        PricePerCoin = 0.0
        skipComputation = 0
        if self.ids['QuantityValue'].text == '' or self.ids['PricePerCoinValue'].text == '': return

        # Extract Quantity 
        if ('%s' % self.ids['QuantityValue'].text).replace('.','').replace(',','').isnumeric():
            Quantity = float(self.ids['QuantityValue'].text.replace(',','.'))
        else:
            self.ids['QuantityValue'].text = '0.0'
            skipComputation = 1

        # Extract Prince Per Coint
        if ('%s' % self.ids['PricePerCoinValue'].text).replace('.','').replace(',','').isnumeric():
            PricePerCoin = float(self.ids['PricePerCoinValue'].text.replace(',','.'))
        else:
            self.ids['PricePerCoinValue'].text = '0.0'
            skipComputation = 1

        # Compute 
        if skipComputation: return
    
        self.ids['TotalSpentValue'].text = str(round((Quantity * PricePerCoin), 2))

class SwapScreen(Screen):
    pass

def show_popup():
    show = P()

    popupWindow = AddAssetTransactionPopup(title_str = 'ADD TRANSACTION')
    popupWindow.open()


if __name__ == "__main__":
    MyApp().run()