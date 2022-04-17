##################
# VERIFY VERSION #
##################
import kivy
from numpy import roots
kivy.require('1.0.9')

###########
# IMPORTS #
###########
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

#####################
# CUSTOM DEFINITION #
#####################
class CustomMenuButton(Button):
    def move_screen(self, App, string):
        print('Moving to ' + string)
        App.root.children[0].children[0].current = string

##############################################
# Contains the setting layout, Menu and Data #
##############################################
class MainLayout(BoxLayout):
    pass

###################################
# Contains the Setting bar on top #
###################################
class SettingLayout(StackLayout):
    pass

#########################################################################
# It will contain the Menu button on the left and the Data on the right #
#########################################################################
class MenuDataLayout(BoxLayout):
    pass

class MenuLayout(StackLayout):
    pass

class DataLayout(BoxLayout):
    pass

########################################
# SCREEN and SCREEN MANAGER DEFINITION #
########################################
class ScreenManagerLayout(ScreenManager):
    pass

class DashboardScreen(Screen):
    pass

class TransactionScreen(Screen):
    pass

class ETFScreen(Screen):
    pass

class StocksScreen(Screen):
    pass

class BondScreen(Screen):
    pass

class CommoditiesScreen(Screen):
    pass

class CryptoScreen(Screen):
    pass

class StatisticsScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

############
# MAIN APP #
############
class FinanceApp(App):
    def build(self):
        return MainLayout()
