##################
# VERIFY VERSION #
##################
import kivy
kivy.require('1.0.9')

DATABASE_PATH = './Database/Data/'

###########################
# IMPORTS FROM CUSTOM LIB #
###########################
import Packages.Configuration.WinConfiguration as WinConf
from Packages.CustomFunction.DefineJsonDatapath import return_updated_data_path
from Packages.DatabaseMng.TransitionManager import Update_account_database_month_year_transition
from Packages.DatabaseMng.TransitionManager import Update_transactions_database_month_year_transition
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.Screens.Dashboard_screen import *
from Packages.Screens.Transaction_screen import *
from Packages.Screens.TransactionList_screen import *
from Packages.Screens.Portfolio_screen import *
from Packages.Screens.Setting_screen import *
from Packages.Screens.Statistics_screen import *
from Packages.Screens.Credits_screen import *
from Packages.Screens.Empty_screen import *
from Packages.Screens.AssetsTransaction_screen import *
from Packages.Screens.Assets_screen import *
from Packages.Screens.MenuLayout import * 
import datetime as dt 
import os

#####################
# IMPORTS FROM KIVY #
#####################
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.app import MDApp

################################################
# Contains the setting layout, Menu and Data   #
# Needed to be defined here, since used in App #
################################################
class MainLayout(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
############
# MAIN APP #
############

# With the build function we declare the root app
class FinanceApp(MDApp):

    def build(self):
        #-- center the window
        # WinConf.SetWindowSize()
        Window.maximize()

        # Internal App data
        self.UserSelectedCurrency = {'Name': 'EUR', 'Symbol' : '€'}
        self.TodayDate_day = dt.datetime.now().strftime("%d") 
        self.TodayDate_month = dt.datetime.now().strftime("%B") 
        self.TodayDate_year = dt.datetime.now().strftime("%Y")

        # Variables used to move among months
        self.VisualizedDate_month = self.TodayDate_month
        self.VisualizedDate_year = self.TodayDate_year

        # Update database to re-check it
        self.check_if_year_month_folder_exists(year = self.VisualizedDate_year, month = self.VisualizedDate_month)

        # Variables to monitor the portfolio under management
        
        # Define the App configuration and Account Database
        self.Configuration_DB = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)
        self.Accounts_DB = AccountsManager_Class(return_updated_data_path(PathManager_Class.database_path), PathManager_Class.Accounts_path)

        return MainLayout()

    def check_if_year_month_folder_exists(self, year: str, month: str):
        # Check if folders exists Data/self.VisualizedDate_year
        if not os.path.exists(DATABASE_PATH + year):
            os.mkdir(DATABASE_PATH + year)

        # Check if folders exists Data/self.VisualizedDate_month
        if not os.path.exists(DATABASE_PATH + year + '/' + month):
            os.mkdir(DATABASE_PATH + year + '/' + month)

    def update_database_class_on_month_change(self):
        # Update the month and year selected
        self.VisualizedDate_month = self.root.children[0].children[1].ids.MonthStringValue.text
        self.VisualizedDate_year = self.root.children[0].children[1].ids.YearStringValue.text

        self.check_if_year_month_folder_exists(year = self.VisualizedDate_year, month = self.VisualizedDate_month)

        Update_account_database_month_year_transition(self.VisualizedDate_month, self.VisualizedDate_year)
        Update_transactions_database_month_year_transition(self.VisualizedDate_month, self.VisualizedDate_year)

        # Update the App configuration and Account Database
        self.Configuration_DB = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)
        self.Accounts_DB = AccountsManager_Class(return_updated_data_path(PathManager_Class.database_path), PathManager_Class.Accounts_path)

        # Let's make sure the new month initial value are the previous month last value

        # Update the current screen
        MDApp.get_running_app().root.children[0].children[0].current_screen.UpdateScreen()

        # Update referenced database
        print('Updating month information')
    
    def on_start(self):
        # Initialize the Dashboard page
        self.root.children[0].children[0].children[0].UpdateScreen()

        # Set the Dashboard button selected
        self.root.children[0].children[1].ids.Dashboard_btn.SelectedStatus = True
        self.root.children[0].children[1].ids.Dashboard_btn.BackgroundColor= self.Configuration_DB.GetElementValue('MenuButtonSelectedBackgroundColor')


    