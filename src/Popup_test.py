from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from kivy.core.window import Window
from kivy.lang import Builder
from Packages.CustomItem.Popup.AddAssetTransactionPopup import AddAssetTransactionPopup
from Packages.CustomItem.Popup.AddTransactionInOutPopup import AddTransactionInOutPopup
from Packages.CustomItem.Popup.AddAccountPopup import AddAccountPopup
import datetime as dt
from Packages.CustomFunction.DefineJsonDatapath import return_updated_data_path

# Designate Out .kv design file
Builder.load_file('Popup_test.kv')

class Widgets(Widget):
    def btn(self):
        show_popup()

class P(FloatLayout):
    pass

class MyApp(MDApp):
    def build(self):
        Window.maximize()

        # Internal App data
        self.UserSelectedCurrency = {'Name': 'EUR', 'Symbol' : '€'}
        self.TodayDate_day = dt.datetime.now().strftime("%d") 
        self.TodayDate_month = dt.datetime.now().strftime("%B") 
        self.TodayDate_year = dt.datetime.now().strftime("%Y")

        # Variables used to move among months
        self.VisualizedDate_month = self.TodayDate_month
        self.VisualizedDate_year = self.TodayDate_year

        # Define the App configuration Database
        self.Configuration_DB = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)
        self.Accounts_DB = JsonManager_Class(return_updated_data_path(PathManager_Class.database_path), PathManager_Class.Accounts_path)
        return Widgets()


def show_popup():
    show = P()

    # popupWindow = AddAssetTransactionPopup(title_str = 'ADD TRANSACTION')
    # popupWindow = AddTransactionInOutPopup(title_str = 'ADD TRANSACTION')
    popupWindow = AddAccountPopup(title_str = 'ADD ACCOUNT')
    popupWindow.open()


if __name__ == "__main__":
    MyApp().run()