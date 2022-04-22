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
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
import DatabaseMng as db_manager

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
path_manager = db_manager.PathManager_Class()

#-- set the actual window size, to be slightly smaller than full screen
def SetWindowSize():
    Window.size = (Win.desiredSize_x, Win.desiredSize_y)
    Window.minimum_width = Win.desiredSize_x
    Window.minimum_height =  Win.desiredSize_y
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

class ModifyButton(Button):
    def __init__(self,**kwargs):
        super().__init__(text = kwargs['text'], size_hint = kwargs['size_hint'])
        self.ManagerOfItem = kwargs['item']
        self.DBManager = kwargs['screen']

    def on_release(self):
        print('Modifying')

class RemoveButton(Button):
    def __init__(self,**kwargs):
        super().__init__(text = kwargs['text'], size_hint = kwargs['size_hint'])
        self.ManagerOfItem = kwargs['item']
        self.ManagerOfScreen = kwargs['screen']
        self.DBManager = kwargs['screen'].InFlow_DBmanager

    def on_release(self):
        # When the remove button is pressed, the item should be removed from the json.
        # The UI shall be updated as well.

        # Remove widget from the Json
        self.DBManager.RemoveElement(self.ManagerOfItem)
        

        # Update the UI
        self.ManagerOfScreen.Update_InFlowBoxLayout()
        pass

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
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        # Initialize the manager of the json manager
        self.InFlow_DBmanager = db_manager.JsonManager_Class(path_manager.database_path,path_manager.Inflow_path)

        # Initilize the InFlowBoxLayout
        # self.Update_InFlowBoxLayout()

    def Update_InFlowBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["'InFlow_counts'"].children[-1]
        self.ids["'InFlow_counts'"].clear_widgets()

        # Add the first item again
        self.ids["'InFlow_counts'"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.InFlow_DBmanager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["'InFlow_counts'"].add_widget(self.Define_InFlowItem(ItemName, Items_dict[ItemName]))

    # Function that add an item in the IN FLOW Box Layout if it does not exist yet
    def Add_Item_InFlow_BoxLayout(self):
        # Open the popup to let the user add the desired Item
        ItemName = 'Poste Italiane'
        ItemDict = [0,0]

        # Add the item to the Json File
        self.InFlow_DBmanager.AddElement({ItemName:ItemDict})

        # Update the BoxLayout
        self.Update_InFlowBoxLayout()

    def Define_InFlowItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        Item = GridLayout(cols=5, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [0.6, None], height = "20dp")
        Item.add_widget(Label(text = ItemName))
        Item.add_widget(Label(text = str(ItemDict[0])))
        Item.add_widget(Label(text = str(ItemDict[1])))
        Item.add_widget(Label(text = str(ItemDict[1]- ItemDict[0])))

        BoxLayoutItem = BoxLayout(orientation = 'horizontal')

        BoxLayoutItem.add_widget(ModifyButton(text = 'M', size_hint = [0.25, 1] , item = ItemName, screen = self))
        BoxLayoutItem.add_widget(RemoveButton(text = 'R', size_hint = [0.25, 1] , item = ItemName, screen = self))
        
        Item.add_widget(BoxLayoutItem)

        return Item

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

class CreditsScreen(Screen):
    pass

############
# MAIN APP #
############
# With the build function we declare the root app
class FinanceApp(App):
    def build(self):
        #-- center the window
        SetWindowSize()
        # Window.borderless = True
        # Window.resizable = False
        return MainLayout()
