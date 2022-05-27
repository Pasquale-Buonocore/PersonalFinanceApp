import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

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

    # Function that opens a popup to add an asset to the category
    def Add_ETF_ETCAssets(self):
        # Initialize the popup
        ETF_ETC_AddAssetPopup = cst_popup.ETF_ETC_AddAssetPopup()
        # Open the Popup
        ETF_ETC_AddAssetPopup.open()
        pass

    # Function that opens the ETF_ETC popup to add item
    def Add_ETF_ETCItem(self):
        # Initialize the popup
        ETF_ETCPopup = cst_popup.ETF_ETCPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        ETF_ETCPopup.open()

    # Define Item to add in the InFlow Box
    def Define_ETF_ETCItem(self, ItemName, ItemDict):
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
        ETF_ETC_ModifyPopup = cst_popup.ETF_ETCPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = ETF_ETC_ModifyPopup))

        # Removing Popup
        ETF_ETC_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.ETF_ETC_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_ETF_ETCBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = ETF_ETC_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_ETF_ETCGraph(self):
        pass
