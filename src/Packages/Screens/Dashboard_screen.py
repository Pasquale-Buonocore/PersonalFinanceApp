import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.CustomItem.WarningPopup as Wrn_popup
import Packages.CustomItem.RemovingPopup as Rm_popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

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
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = InFlow_ModifyPopup))

        # Removing Popup
        InFlow_RemovePopup = Rm_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.InFlow_DBManager, UpdateFunction_str= 'Update_InFlowBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = InFlow_RemovePopup))
        
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
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Expences_ModifyPopup))

        # Removing Popup
        Expences_RemovePopup = Rm_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Expences_DBManager, UpdateFunction_str= 'Update_ExpencesBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Expences_RemovePopup))
        
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
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Earnings_ModifyPopup))

        # Removing Popup
        Earnings_RemovePopup = Rm_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Earnings_DBManager, UpdateFunction_str= 'Update_EarningsBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Earnings_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item
    
    # Given the JsonFile, create a graph to display for the Earnings graph
    def Update_EarningGraph(self):
        pass
