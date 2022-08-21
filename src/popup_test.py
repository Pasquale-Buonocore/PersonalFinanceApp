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
    
    def OpenDatePicker(self):
        print('Opening Date Picker')

    def OpeningAddFee(self):
        # Define Popup
        Popup = AddFeePopup()
        Popup.open()
    
    def OpeningAddNote(self):
        # Define Popup
        Popup = AddNotePopup()
        Popup.open()

    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('DateFeeNoteBtnSelectedBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('DateFeeNoteBtnNotSelectedBackgroundColor') 

class AddAssetTransactionPopup(ModalView):
    def __init__(self, title_str = ''): 
        # Setting internal attributes
        self.title = title_str

        # Initialize the super class
        super().__init__(size_hint = (0.35,0.7))

        # Modify BUY button as selected one
        self.ids['BUY_BTN'].SelectedStatus = True
        self.ids['BUY_BTN'].BackgroundColor = self.ids['BUY_BTN'].Configuration.GetElementValue('MenuButtonSelectedBackgroundColor')

class BuySellScreen(Screen):
    pass

class SwapScreen(Screen):
    pass

def show_popup():
    show = P()

    popupWindow = AddAssetTransactionPopup(title_str = 'ADD TRANSACTION')
    popupWindow.open()


if __name__ == "__main__":
    MyApp().run()