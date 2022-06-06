import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class StocksScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize the manager of the json manager
        self.Stocks_DBManager = db_manager.JsonManagerList_Class(db_manager.path_manager.database_path,db_manager.path_manager.Stocks_path)
        
    def UpdateScreen(self):
        self.Update_StocksBoxLayout()

    #####################
    #    STOCKS  BOX    #
    #####################

    # Update the Stocks Box Layout
    def Update_StocksBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["Stocks"].children[-1]
        self.ids["Stocks"].clear_widgets()

        # Add the first item again
        self.ids["Stocks"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.Stocks_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["Stocks"].add_widget(self.Define_StocksItem(ItemName, Items_dict[ItemName] ))

        # Update the InFlowGraph
        self.Update_StocksGraph()

    # Function that opens the Stocks popup to add item
    def Add_StocksItem(self):
        # Initialize the popup
        StocksPopup = cst_popup.StocksPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        StocksPopup.open()

    # Define Item to add in the InFlow Box
    def Define_StocksItem(self, ItemName, ItemDict):
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
        Stocks_ModifyPopup = cst_popup.StocksPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Stocks_ModifyPopup))

        # Removing Popup
        Stocks_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Stocks_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_StocksBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Stocks_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_StocksGraph(self):
        pass
