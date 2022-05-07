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
        # Update current screen name
        App.root.children[0].children[0].current = string
        # Update current screen
        App.root.children[0].children[0].current_screen.UpdateScreen()

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
        self.InFlow_DBManager = db_manager.JsonManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Inflow_path)
        self.Expences_DBManager = db_manager.JsonManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Expences_path)
        self.Earnings_DBManager = db_manager.JsonManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Income_path)
    
    # Function to call when the screen is changed to Dashboard
    def UpdateScreen(self):
        # Update the dashboard screen 
        self.Update_InFlowBoxLayout()
        self.Update_ExpencesBoxLayout()
        self.Update_EarningsBoxLayout()

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
        Items_dict = self.InFlow_DBManager.ReadJson()

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
        InFlow_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.InFlow_DBManager, UpdateFunction_str= 'Update_InFlowBoxLayout')
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

    #####################
    #    EARNING BOX    #
    #####################

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
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize the manager of the json manager
        self.TransactionIn_DBManager = db_manager.JsonManagerList_Class(db_manager.path_manager.database_path,db_manager.path_manager.TransactionIn_path)
        self.TransactionOut_DBManager = db_manager.JsonManagerList_Class(db_manager.path_manager.database_path,db_manager.path_manager.TransactionOut_path)

    def UpdateScreen(self):
        self.Update_TransactionInBoxLayout()
        self.Update_TransactionOutBoxLayout()

    #############################
    #    TRANSACTION IN  BOX    #
    #############################

    # Update the TransactionIn Box Layout
    def Update_TransactionInBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["TransactionIn"].children[-1]
        self.ids["TransactionIn"].clear_widgets()

        # Add the first item again
        self.ids["TransactionIn"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.TransactionIn_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["TransactionIn"].add_widget(self.Define_TransactionInItem(ItemName, Items_dict[ItemName] ))

        # Update the InFlowGraph
        self.Update_TransactionInGraph()

    # Function that opens the TransactionIn popup to add item
    def Add_TransactionInItem(self):
        # Initialize the popup
        TransactionInPopup = cst_popup.TransactionInPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        TransactionInPopup.open()

    # Define Item to add in the InFlow Box
    def Define_TransactionInItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        # Item = GridLayout(id = ItemName , cols=7, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item = GridLayout(cols=7, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item.add_widget(Label(text = str(ItemDict[0]), size_hint = [0.15,1])) # Data
        Item.add_widget(Label(text = str(ItemDict[1]), size_hint = [0.15,1])) # Amount
        Item.add_widget(Label(text = str(ItemDict[2]), size_hint = [0.15,1])) # Category
        Item.add_widget(Label(text = str(ItemDict[3]), size_hint = [0.3,1])) # Description
        Item.add_widget(Label(text = str(ItemDict[4]), size_hint = [0.15,1])) # Paid with       

        BoxLayoutItem = BoxLayout(orientation = 'horizontal', size_hint = [0.1, 1])

        # Modify Popup
        TransactionIn_ModifyPopup = cst_popup.TransactionInPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = TransactionIn_ModifyPopup))

        # Removing Popup
        TransactionIn_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.TransactionIn_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_TransactionInBoxLayout')
        BoxLayoutItem.add_widget(RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = TransactionIn_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_TransactionInGraph(self):
        pass

    ##############################
    #    TRANSACTION OUT  BOX    #
    ##############################

    # Update the TransactionOut Box Layout
    def Update_TransactionOutBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["TransactionOut"].children[-1]
        self.ids["TransactionOut"].clear_widgets()

        # Add the first item again
        self.ids["TransactionOut"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.TransactionOut_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["TransactionOut"].add_widget(self.Define_TransactionOutItem(ItemName, Items_dict[ItemName]))

        # Update the InFlowGraph
        self.Update_TransactionOutGraph()

    # Function that opens the TransactionOut popup to add item
    def Add_TransactionOutItem(self):
        # Initialize the popup
        TransactionOutPopup = cst_popup.TransactionOutPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        TransactionOutPopup.open()

    # Define Item to add in the InFlow Box
    def Define_TransactionOutItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        Item = GridLayout(cols=7, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item.add_widget(Label(text = str(ItemDict[0]), size_hint = [0.15,1])) # Data
        Item.add_widget(Label(text = str(ItemDict[1]), size_hint = [0.15,1])) # Amount
        Item.add_widget(Label(text = str(ItemDict[2]), size_hint = [0.15,1])) # Category
        Item.add_widget(Label(text = str(ItemDict[3]), size_hint = [0.3,1])) # Description
        Item.add_widget(Label(text = str(ItemDict[4]), size_hint = [0.15,1])) # Paid with       

        BoxLayoutItem = BoxLayout(orientation = 'horizontal', size_hint = [0.1, 1])

        # Modify Popup
        TransactionOut_ModifyPopup = cst_popup.TransactionOutPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = TransactionOut_ModifyPopup))

        # Removing Popup
        TransactionOut_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.TransactionOut_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_TransactionOutBoxLayout')
        BoxLayoutItem.add_widget(RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = TransactionOut_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_TransactionOutGraph(self):
        pass

class ETFScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize the manager of the json manager
        self.ETF_ETC_DBManager = db_manager.JsonManagerList_Class(db_manager.path_manager.database_path,db_manager.path_manager.ETF_ETC_path)
        
    def UpdateScreen(self):
        self.Update_ETF_ETCBoxLayout()

    ######################
    #    ETF ETC  BOX    #
    ######################

    # Update the ETF_ETC Box Layout
    def Update_ETF_ETCBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["ETF_ETC"].children[-1]
        self.ids["ETF_ETC"].clear_widgets()

        # Add the first item again
        self.ids["ETF_ETC"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.ETF_ETC_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["ETF_ETC"].add_widget(self.Define_ETF_ETCItem(ItemName, Items_dict[ItemName] ))

        # Update the InFlowGraph
        self.Update_ETF_ETCGraph()

    # Function that opens the ETF_ETC popup to add item
    def Add_ETF_ETCItem(self):
        # Initialize the popup
        ETF_ETCPopup = cst_popup.ETF_ETCPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        ETF_ETCPopup.open()

    # Define Item to add in the InFlow Box
    def Define_ETF_ETCItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        # Item = GridLayout(id = ItemName , cols=7, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item = GridLayout(cols= 8, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item.add_widget(Label(text = str(ItemDict[0]), size_hint = [0.3,1])) # Name
        Item.add_widget(Label(text = str(ItemDict[1]), size_hint = [0.1,1])) # Symbol
        Item.add_widget(Label(text = str(ItemDict[2]), size_hint = [0.1,1])) # Data
        Item.add_widget(Label(text = str(ItemDict[3]), size_hint = [0.1,1])) # Type
        Item.add_widget(Label(text = str(ItemDict[4]), size_hint = [0.1,1])) # Broker
        Item.add_widget(Label(text = str(ItemDict[5]), size_hint = [0.1,1]))  # Quantity
        Item.add_widget(Label(text = str(ItemDict[7]), size_hint = [0.1,1])) # Total spend      

        BoxLayoutItem = BoxLayout(orientation = 'horizontal', size_hint = [0.1, 1])

        # Modify Popup
        ETF_ETC_ModifyPopup = cst_popup.ETF_ETCPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = ETF_ETC_ModifyPopup))

        # Removing Popup
        ETF_ETC_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.ETF_ETC_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_ETF_ETCBoxLayout')
        BoxLayoutItem.add_widget(RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = ETF_ETC_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_ETF_ETCGraph(self):
        pass

class StocksScreen(Screen):
    def UpdateScreen(self):
        pass

class BondScreen(Screen):
    def UpdateScreen(self):
        pass

class CommoditiesScreen(Screen):
    def UpdateScreen(self):
        pass

class CryptoScreen(Screen):
    def UpdateScreen(self):
        pass

class StatisticsScreen(Screen):
    def UpdateScreen(self):
        pass

class SettingScreen(Screen):
    def UpdateScreen(self):
        pass

class CreditsScreen(Screen):
    def UpdateScreen(self):
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
        self.root.children[0].children[0].children[0].UpdateScreen()
