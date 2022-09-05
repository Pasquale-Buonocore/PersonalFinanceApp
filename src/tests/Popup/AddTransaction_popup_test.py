from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from kivy.core.window import Window
from kivy.lang import Builder
from Packages.CustomItem.Popup.AddAssetTransactionPopup import AddAssetTransactionPopup
from Packages.CustomItem.Popup.AddTransactionInOutPopup import AddTransactionInOutPopup
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

    # popupWindow = AddAssetTransactionPopup(title_str = 'ADD TRANSACTION')
    popupWindow = AddTransactionInOutPopup(title_str = 'ADD TRANSACTION')
    popupWindow.open()


if __name__ == "__main__":
    MyApp().run()