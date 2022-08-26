from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
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
from Packages.CustomItem.DataPicker.DataPickerItem import MDDatePicker
from Packages.CustomItem.SelectAccountPopup import SelectAccountPopup
from Packages.CustomItem.Popup.AddAssetTransactionPopup import AddAssetTransactionPopup
import datetime as dt

# Designate Out .kv design file
Builder.load_file('AddTransaction_popup_test.kv')

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


def show_popup():
    show = P()

    popupWindow = AddAssetTransactionPopup(title_str = 'ADD TRANSACTION')
    popupWindow.open()


if __name__ == "__main__":
    MyApp().run()