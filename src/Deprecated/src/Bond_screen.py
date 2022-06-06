import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class BondScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize the manager of the json manager
        self.Bonds_DBManager = db_manager.JsonManagerList_Class(db_manager.path_manager.database_path,db_manager.path_manager.Bonds_path)
        
    def UpdateScreen(self):
        self.Update_BondsBoxLayout()

    ####################
    #    BONDS  BOX    #
    ####################

    # Update the Bonds Box Layout
    def Update_BondsBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["Bonds"].children[-1]
        self.ids["Bonds"].clear_widgets()

        # Add the first item again
        self.ids["Bonds"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.Bonds_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["Bonds"].add_widget(self.Define_BondsItem(ItemName, Items_dict[ItemName] ))

        # Update the InFlowGraph
        self.Update_BondsGraph()

    # Function that opens the Bonds popup to add item
    def Add_BondsItem(self):
        # Initialize the popup
        BondsPopup = cst_popup.BondsPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        BondsPopup.open()

    # Define Item to add in the InFlow Box
    def Define_BondsItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
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
        Bonds_ModifyPopup = cst_popup.BondsPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Bonds_ModifyPopup))

        # Removing Popup
        Bonds_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Bonds_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_BondsBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Bonds_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_BondsGraph(self):
        pass
