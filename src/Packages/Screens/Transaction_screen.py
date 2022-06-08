import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.CustomItem.RemovingPopup as Rm_popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

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
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = TransactionIn_ModifyPopup))

        # Removing Popup
        TransactionIn_RemovePopup = Rm_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.TransactionIn_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_TransactionInBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = TransactionIn_RemovePopup))
        
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
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = TransactionOut_ModifyPopup))

        # Removing Popup
        TransactionOut_RemovePopup = Rm_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.TransactionOut_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_TransactionOutBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = TransactionOut_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_TransactionOutGraph(self):
        pass
