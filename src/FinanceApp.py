##################
# VERIFY VERSION #
##################
import kivy
kivy.require('1.0.9')

###########################
# IMPORTS FROM CUSTOM LIB #
###########################
import Packages.Configuration.WinConfiguration as WinConf
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
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

#####################
# IMPORTS FROM KIVY #
#####################
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.app import App

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
        WinConf.SetWindowSize()

        # Define the App configuration Database
        self.Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)

        return MainLayout()

    def on_start(self):
        # Initialize the Dashboard page
        self.root.children[0].children[0].children[0].UpdateScreen()

        # Set the Dashboard button selected
        self.root.children[0].children[1].children[-2].SelectedStatus = True
        self.root.children[0].children[1].children[-2].background_color = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor')

        # Set the menu button images
        for element in self.root.children[0].children[1].children:
            # Set Image for each class and update image
            ImageName = element.text.strip().lower()
            element.ImageName = 'images/button/' + ImageName + '.png'
            element.source = 'images/button/' + ImageName + '.png'

