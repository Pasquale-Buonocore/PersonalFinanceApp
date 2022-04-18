##################
# VERIFY VERSION #
##################
import kivy
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
from kivy.core.window import Window

#-- maximize first, to get the screen size, minus any OS toolbars
class WindowInfos():
    def __init__(self):
        Window.maximize()
        self.maxSize = Window.system_size
        self.desiredSize_x = self.maxSize[0]*0.9
        self.desiredSize_y = self.maxSize[1]*0.9
        self.left = (self.maxSize[0] -self.desiredSize_x)*0.5
        self.top = (self.maxSize[1] - self.desiredSize_y)*0.5

Win = WindowInfos()

#-- set the actual window size, to be slightly smaller than full screen
def SetWindowSize():
    Window.size = (Win.desiredSize_x, Win.desiredSize_y)
    Window.left = Win.left
    Window.top = Win.top
    
#####################
# CUSTOM DEFINITION #
#####################
class CustomMenuButton(Button):
    def move_screen(self, App, string):
        print('Moving to ' + string)
        App.root.children[0].children[0].current = string
    
    def add_button(self, App):
        print('Adding button to ScrollView')
        b1 = Button(text = 'B', size_hint = (1, None), size= ("100dp", "100dp"))
        App.root.children[0].children[0].screens[0].children[0].children[0].children[0].add_widget(b1)

##############################################
# Contains the setting layout, Menu and Data #
##############################################
class MainLayout(BoxLayout):
    pass

###################################
# Contains the Setting bar on top #
###################################
class SettingLayout(StackLayout):
    def minimize_window(self):
        Window.minimize()
    
    def restore_window(self):
        SetWindowSize()

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
# With the build function we declare the root app
class FinanceApp(App):
    def build(self):

        #-- center the window
        SetWindowSize()

        Window.borderless = True
        return MainLayout()
