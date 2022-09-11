import Packages.DatabaseMng.JsonManager as json_manager
from kivymd.app import MDApp
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.CustomItem.Popup.WarningPopup as Wrn_popup
import Packages.CustomItem.Popup.RemovingPopup as Rm_popup
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from Packages.DatabaseMng.AccountsManager import AccountsManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.CustomItem.Lists.AccountsListManagement import AccountRowBoxLayout, AccountRowBoxLayout_Title, AddNewAccountBoxLayout, AccountRowExpandedBoxLayout

class DashboardScreen(Screen):
    image_source = StringProperty('images/Support/AssetsInPortfolio.png')

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize internal data
        self.AccountsBoxLayout = 'AccountsBoxLayout'
        
    # Function to call when the screen is changed to Dashboard
    def UpdateScreen(self):
        self.ids.GraphPortfolioAllocation.source = 'images/Support/AssetsInPortfolio.png'
        self.ids.GraphPortfolioAllocation.reload()

        self.ids.GraphAssetAllocation.source = 'images/Support/AssetsInPortfolio.png'
        self.ids.GraphAssetAllocation.reload()

        # Update the dashboard screen
        self.Update_AccountBoxLayout()
        self.Update_InFlowBoxLayout()
        self.Update_ExpencesBoxLayout()
        self.Update_EarningsBoxLayout()

    ########################
    #      INFLOW BOX      #
    ########################

    # Update the In Flow Box Layout
    def Update_InFlowBoxLayout(self):
        return 

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
        return

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
        return 
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

    #######################
    # ACCOUNTS MANAGEMENT #
    #######################
    
    # Update the list of accounts
    def Update_AccountBoxLayout(self):
        json_file = MDApp.get_running_app().Accounts_DB.ReadJson()

        # Clear the Item inside the BoxLayout (Keep the first element only)
        self.ids[self.AccountsBoxLayout].clear_widgets()
        
        InfoDict = {'Currency': ''}
        InfoDict.update({'AccountName' : 'ACCOUNT NAME'})
        InfoDict.update({'Category' : 'CATEGORY'})
        InfoDict.update({'LastMonthValue' : 'LAST MONTH VALUE'})
        InfoDict.update({'ActualMonthValue' : 'CURRENT VALUE'})
        InfoDict.update({'ValueDifference' : 'DIFFERENCE'})
        InfoDict.update({'RowHeight': "20dp"})

        # Append to the account list
        self.ids[self.AccountsBoxLayout].add_widget(AccountRowBoxLayout_Title(kwargs = InfoDict))

        for account in json_file.keys():
            InfoDict = {'Currency': json_file[account]['Statistics']['Symbol']}
            InfoDict.update({'AccountName' : account})
            InfoDict.update({'Category' : json_file[account]['Statistics']['Category']})
            InfoDict.update({'LastMonthValue' : json_file[account]['Statistics']['LastMonthValue']})
            InfoDict.update({'ActualMonthValue' : json_file[account]['Statistics']['ActualMonthValue']})
            InfoDict.update({'ValueDifference' : float(InfoDict['ActualMonthValue']) - float(InfoDict['LastMonthValue'])})
            InfoDict.update({'RowHeight': "40dp"})

            # Append to the account list
            self.ids[self.AccountsBoxLayout].add_widget(AccountRowBoxLayout(kwargs = InfoDict))

        self.ids[self.AccountsBoxLayout].add_widget(AddNewAccountBoxLayout())

    def UpdateExpandedAccountList(self):
        ListOfWidget = self.ids[self.AccountsBoxLayout].children.copy()
        ListOfWidget.reverse()

        self.ids[self.AccountsBoxLayout].clear_widgets()

        for children in ListOfWidget:
            if hasattr(children, 'RowExpansion'): continue

            self.ids[self.AccountsBoxLayout].add_widget(children)
            if children.ToExpand:
                self.ids[self.AccountsBoxLayout].add_widget(AccountRowExpandedBoxLayout())