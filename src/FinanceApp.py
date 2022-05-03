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
import CustomPopup as cst_popup

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
        self.Popup = kwargs['Popup']

    def on_release(self):
        # Open the Popup
        self.Popup.open()

class RemoveButton(Button):
    def __init__(self,**kwargs):
        super().__init__(text = kwargs['text'], size_hint = kwargs['size_hint'])
        self.Popup = kwargs['Popup']

    def on_release(self):
        # Open the popup
        self.Popup.open()

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
        self.InFlow_DBmanager = db_manager.JsonManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Inflow_path)
        self.Expences_DBManager = db_manager.JsonManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Expences_path)
        self.Earnings_DBManager = db_manager.JsonManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Income_path)

    ########################
    #      INFLOW BOX      #
    ########################

    # Update the In Flow Box Layout
    def Update_InFlowBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["InFlow_counts"].children[-1]
        self.ids["InFlow_counts"].clear_widgets()

        # Add the first item again
        self.ids["InFlow_counts"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.InFlow_DBmanager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["InFlow_counts"].add_widget(self.Define_InFlowItem(ItemName, Items_dict[ItemName]))
        
        # Update the InFlowGraph
        self.Update_InFlowGraph()

    # Function that opens the Inflow popup
    def Add_InFlowItem(self):
        # Initialize the popup
        InFlowPopup = cst_popup.InFlowPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        InFlowPopup.open()

    # Define Item to add in the InFlow Box
    def Define_InFlowItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        Item = GridLayout(cols=5, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item.add_widget(Label(text = ItemName))
        Item.add_widget(Label(text = str(ItemDict[0])))
        Item.add_widget(Label(text = str(ItemDict[1])))
        Item.add_widget(Label(text = str(ItemDict[1]- ItemDict[0])))

        BoxLayoutItem = BoxLayout(orientation = 'horizontal')

        # Modify Popup
        InFlow_ModifyPopup = cst_popup.InFlowPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = InFlow_ModifyPopup))

        # Removing Popup
        InFlow_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.InFlow_DBmanager, UpdateFunction_str= 'Update_InFlowBoxLayout')
        BoxLayoutItem.add_widget(RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = InFlow_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_InFlowGraph(self):
        pass
    
    ######################
    #    EXPENCES BOX    #
    ######################

    # Update the Expences Box Layout
    def Update_ExpencesBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["Expenses"].children[-1]
        self.ids["Expenses"].clear_widgets()

        # Add the first item again
        self.ids["Expenses"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.Expences_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["Expenses"].add_widget(self.Define_ExpencesItem(ItemName, Items_dict[ItemName]))
        
        # Update the InFlowGraph
        self.Update_ExpencesGraph()

    # Function that opens the Expences popup
    def Add_ExpencesItem(self):
        # Initialize the popup
        ExpencesPopup = cst_popup.ExpencesPopup('ADD EXPENCES ITEM POPUP', type ='A')
        # Open the Popup
        ExpencesPopup.open()
    
    # Define Item to add in the expences Box
    def Define_ExpencesItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        Item = GridLayout(cols=5, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item.add_widget(Label(text = ItemName))
        Item.add_widget(Label(text = str(ItemDict[0])))
        Item.add_widget(Label(text = str(ItemDict[1])))
        Item.add_widget(Label(text = str(ItemDict[1]- ItemDict[0])))

        BoxLayoutItem = BoxLayout(orientation = 'horizontal')

        # Modify Popup
        Expences_ModifyPopup = cst_popup.ExpencesPopup(title_str = 'MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Expences_ModifyPopup))

        # Removing Popup
        Expences_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Expences_DBManager, UpdateFunction_str= 'Update_ExpencesBoxLayout')
        BoxLayoutItem.add_widget(RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Expences_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item
    
    # Given the JsonFile, create a graph to display for the expences graph
    def Update_ExpencesGraph(self):
        pass

    ######################
    #    EEARNING BOX    #
    ######################

    # Update the Earning Box Layout
    def Update_EarningsBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["Earnings"].children[-1]
        self.ids["Earnings"].clear_widgets()

        # Add the first item again
        self.ids["Earnings"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.Earnings_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["Earnings"].add_widget(self.Define_EarningItem(ItemName, Items_dict[ItemName]))
        
        # Update the InFlowGraph
        self.Update_EarningGraph()

    # Function that opens the Earnings popup
    def Add_EarningsItem(self):
        # Initialize the popup
        EarningPopup = cst_popup.EarningsPopup('ADD EARNING ITEM POPUP', type ='A')
        # Open the Popup
        EarningPopup.open()
    
    # Define Item to add in the Earnings Box
    def Define_EarningItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        Item = GridLayout(cols=5, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item.add_widget(Label(text = ItemName))
        Item.add_widget(Label(text = str(ItemDict[0])))
        Item.add_widget(Label(text = str(ItemDict[1])))
        Item.add_widget(Label(text = str(ItemDict[1]- ItemDict[0])))

        BoxLayoutItem = BoxLayout(orientation = 'horizontal')

        # Modify Popup
        Earnings_ModifyPopup = cst_popup.EarningsPopup(title_str = 'MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Earnings_ModifyPopup))

        # Removing Popup
        Earnings_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Earnings_DBManager, UpdateFunction_str= 'Update_EarningsBoxLayout')
        BoxLayoutItem.add_widget(RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Earnings_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item
    
    # Given the JsonFile, create a graph to display for the Earnings graph
    def Update_EarningGraph(self):
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
    
    def on_start(self):
        # Initialize the Dashboard page
        self.root.children[0].children[0].children[0].Update_InFlowBoxLayout()
        self.root.children[0].children[0].children[0].Update_ExpencesBoxLayout()
        self.root.children[0].children[0].children[0].Update_EarningsBoxLayout()
