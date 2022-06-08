##################
# VERIFY VERSION #
##################
import kivy
kivy.require('1.0.9')

###########################
# IMPORTS FROM CUSTOM LIB #
###########################
import Packages.Configuration.WinConfiguration as WinConf
import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
from Packages.Screens.Dashboard_screen import *
from Packages.Screens.Transaction_screen import *
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
from kivy.app import App

################################################
# Contains the setting layout, Menu and Data   #
# Needed to be defined here, since used in App #
################################################
class MainLayout(BoxLayout):
    pass

###################################
# Contains the Setting bar on top #
###################################
class SettingLayout(StackLayout):
    def minimize_window(self):
        Window.minimize()
    
    def restore_window(self):
        WinConf.SetWindowSize()

############
# MAIN APP #
############

# With the build function we declare the root app
class FinanceApp(App):

    def build(self):
        #-- center the window
        WinConf.SetWindowSize()

        # Bind function to window resizing
        Window.bind(on_resize = self.UpdatePortfolioView)

        return MainLayout()
    
    def UpdatePortfolioView(self, window, width, height):
        if self.root.children[0].children[0].current == 'CRYPTO':
            # Analysis has to continue!
            # self.root.children[0].children[1].children[0].move_screen(self, 'CREDITS')
            # self.root.children[0].children[1].children[5].move_screen(self, 'CRYPTO')
            pass

    def on_start(self):
        # Initialize the Dashboard page
        self.root.children[0].children[0].children[0].UpdateScreen()

        # Set the Dashboard button selected
        self.root.children[0].children[1].children[-2].SelectedStatus = True
        self.root.children[0].children[1].children[-2].background_color = [0.2,0.2,1,1]

        # Set the menu button images
        for element in self.root.children[0].children[1].children:
            # Set Image for each class and update image
            ImageName = element.text.strip().lower()
            element.ImageName = 'images/button/' + ImageName + '.png'
            element.source = 'images/button/' + ImageName + '.png'

