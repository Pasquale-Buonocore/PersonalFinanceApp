import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class PortfoliosScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize the manager of the json manager
        self.Crypto_DBManager = db_manager.JsonManagerList_Class(db_manager.path_manager.database_path,db_manager.path_manager.Crypto_path)
        self.CryptoAssets_DBManager = db_manager.JsonManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.CryptoAssets_path)
        
    def UpdateScreen(self):
        self.Update_CryptoBoxLayout()
        self.Update_CryptoAssetsList()
        
    #####################
    #    CRYPTO  BOX    #
    #####################

    ###################
    # ASSE ALLOCATION #
    ###################

    # Function that opens a popup to add an asset to the category
    def Add_CryptoAssets(self):
        # Initialize the popup
        Add_CryptoAssets = cst_popup.Add_CryptoAssetsPopup('ADD ASSET POPUP',type = 'A')
        # Open the Popup
        Add_CryptoAssets.open()

    # Function that updates the Crypto Assets lvl
    def Compute_CryptoAssetsList(self, NameValue, SymbolValue):
        # Given the NameValue and SymbolValue, the functions pars all transaction returnings:
        # Total Quantity, Buy Avarage price, Current Price, Market Value, Performances
        TotalQuantity = 0
        AvaragePrice = 0 
        CurrentPrice = 0
        MarketValue = 0
        Performance = 0
        return {NameValue:[SymbolValue, TotalQuantity, AvaragePrice, CurrentPrice, MarketValue, Performance]}
    
    def Update_CryptoAssetsList(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["Crypto_Assets"].children[-1]
        self.ids["Crypto_Assets"].clear_widgets()

        # Add the first item again
        self.ids["Crypto_Assets"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.CryptoAssets_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["Crypto_Assets"].add_widget(self.Define_CryptoAssetsItem(ItemName, Items_dict[ItemName]))

    def Define_CryptoAssetsItem(self, ItemName, ItemDict):
        # Compute Item to Append according to the structure defined
        Item = GridLayout(cols= 8, rows = 1, padding = ("30dp", "0dp", "30dp", "0dp"), size_hint = [1, None], height = "20dp")
        Item.add_widget(Label(text = ItemName, size_hint = [0.3,1])) # Name
        Item.add_widget(Label(text = str(ItemDict[0]), size_hint = [0.1,1])) # Symbol
        Item.add_widget(Label(text = str(ItemDict[1]), size_hint = [0.1,1])) # Quantity
        Item.add_widget(Label(text = str(ItemDict[2]), size_hint = [0.1,1])) # Avarage price
        Item.add_widget(Label(text = str(ItemDict[3]), size_hint = [0.1,1])) # Current Price
        Item.add_widget(Label(text = str(ItemDict[4]), size_hint = [0.1,1])) # Market Value
        Item.add_widget(Label(text = str(ItemDict[5]), size_hint = [0.1,1])) # Performance 
        
        BoxLayoutItem = BoxLayout(orientation = 'horizontal', size_hint = [0.1, 1])

        # Modify Popup
        Crypto_AssetModifyPopup = cst_popup.Add_CryptoAssetsPopup('MODIFY ASSET POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Crypto_AssetModifyPopup))

        # Removing Popup
        Crypto_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.CryptoAssets_DBManager, RemoveFunction = 'RemoveElement', UpdateFunction_str= 'Update_CryptoAssetsList')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Crypto_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    ################
    # TRANSACTIONS #
    ################
    # Update the Crypto Box Layout
    def Update_CryptoBoxLayout(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        First_widget = self.ids["Crypto"].children[-1]
        self.ids["Crypto"].clear_widgets()

        # Add the first item again
        self.ids["Crypto"].add_widget(First_widget)

        # Read the Json file
        Items_dict = self.Crypto_DBManager.ReadJson()

        # Add Item in the Json to the 
        for ItemName in Items_dict.keys():
            self.ids["Crypto"].add_widget(self.Define_CryptoItem(ItemName, Items_dict[ItemName] ))

        # Update the InFlowGraph
        self.Update_CryptoGraph()

    # Function that opens the Crypto popup to add item
    def Add_CryptoItem(self):
        # Initialize the popup
        CryptoPopup = cst_popup.CryptoPopup('ADD ITEM POPUP',type = 'A')
        # Open the Popup
        CryptoPopup.open()

    # Define Item to add in the InFlow Box
    def Define_CryptoItem(self, ItemName, ItemDict):
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
        Crypto_ModifyPopup = cst_popup.CryptoPopup('MODIFY ITEM POPUP', type ='M', itemToMod = {ItemName:ItemDict})
        BoxLayoutItem.add_widget(cst_item.ModifyButton(text = 'M', size_hint = [0.25, 1], Popup = Crypto_ModifyPopup))

        # Removing Popup
        Crypto_RemovePopup = cst_popup.RemovingPopup(ManagerOfItem = ItemName, ManagerOfScreen = self, DBManager = self.Crypto_DBManager, RemoveFunction = 'RemoveElementFromList', UpdateFunction_str= 'Update_CryptoBoxLayout')
        BoxLayoutItem.add_widget(cst_item.RemoveButton(text = 'R', size_hint = [0.25, 1] , Popup = Crypto_RemovePopup))
        
        Item.add_widget(BoxLayoutItem)

        return Item

    # Given the JsonFile, create a graph to display for the In flow graph
    def Update_CryptoGraph(self):
        pass
