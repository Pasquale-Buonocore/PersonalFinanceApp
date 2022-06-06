import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class CommoditiesScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize the manager of the json manager
        self.Commodities_DBManager = db_manager.JsonManagerList_Class(db_manager.path_manager.database_path,db_manager.path_manager.Commodities_path)
        
    def UpdateScreen(self):
        self.Update_CommoditiesBoxLayout()

    ##########################
    #    COMMODITIES  BOX    #
    ##########################

    # Update the Commodities Box Layout
    def Update_CommoditiesBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["Commodities"].children[-1]
        self.ids["Commodities"].clear_widgets()

        # Add the first item again
        self.ids["Commodities"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.Commodities_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["Commodities"].add_widget(self.Define_CommoditiesItem(ItemName, Items_dict[ItemName] ))

        # Update the InFlowGraph
        self.Update_CommoditiesGraph()

    # Function that opens the Commodities popup to add item
    def Add_CommoditiesItem(self):
        # Initialize the popup
        CommoditiesPopup = cst_popup.CommoditiesPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        CommoditiesPopup.open()

    # Define Item to add in the InFlow Box
    def Define_CommoditiesItem(self, ItemName, ItemDict):
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
        Commodities_ModifyPopup = cst_popup.CommoditiesPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Commodities_ModifyPopup))

        # Removing Popup
        Commodities_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Commodities_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_CommoditiesBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Commodities_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_CommoditiesGraph(self):
        pass
