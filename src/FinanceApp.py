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

######################
# CLASSES DEFINITION #
######################

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

############
# MAIN APP #
############
class FinanceApp(App):
    def build(self):
        return MainLayout()
