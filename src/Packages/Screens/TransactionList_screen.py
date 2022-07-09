import Packages.DatabaseMng.JsonManagerList as jsonList_manager
import Packages.CustomItem.AddTransactionInOutPopup as TransInOut_Popup
import Packages.CustomItem.RemoveTransactionInOutPopup as RemoveTransactionInOutPopup
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.CustomItem.RemovingPopup as Rm_popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label

class TransactionListScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        # Store info of the Box Layout to fill in
        self.ScreenToUpdate = 'AssetsTransactionHeader'
    
    # Function to call when moving towards that page
    def UpdateScreen(self, portfolio, Database):
        self.ids.TransactionListLabel.text = 'TRANSACTION ' + portfolio.upper()
        self.DBManager = Database
        self.portfolio = portfolio

        # Update Screen
        self.UpdateListOfTransaction()

    # Update the list of transaction given the portafolio name
    def UpdateListOfTransaction(self):
        json_file = self.DBManager.ReadJson()
        
        # Clear the Item inside the BoxLayout (Keep the first element only)
        self.ids[self.ScreenToUpdate].clear_widgets()

        # Size dello ScreenManager
        ScreenManagerSize_x = self.parent.size[0]
        BoxLayoutPadding_ls= self.children[0].children[0].padding[0]
        BoxLayoutPadding_rs = self.children[0].children[0].padding[2]
        text_size = ScreenManagerSize_x - BoxLayoutPadding_ls - BoxLayoutPadding_rs

        for asset in json_file[self.portfolio]['Assets'].keys():
            for transaction_idx in json_file[self.portfolio]['Assets'][asset]['Transactions']:
                transaction = json_file[self.portfolio]['Assets'][asset]['Transactions'][transaction_idx]
                # Get the Currency of such transaction
                Currency_str = transaction['Currency']

                # Append to the transaction list
                self.ids[self.ScreenToUpdate].add_widget(self.DefineFullTransaction(textsize = text_size, asset = asset, TransactionDict = transaction, Index = transaction_idx , Currency = Currency_str))
    
        if not len(self.ids[self.ScreenToUpdate].children):
            # Add empty item to the widget
            self.ids[self.ScreenToUpdate].add_widget(self.DefineEmptyTransaction(textsize = text_size))

 # Define and empty transaction with "EMPTY" Label
    def DefineEmptyTransaction(self, textsize):
        # Get the necessary information from the AssetDictionary
        GraphicToReturn = RelativeLayout()
        GraphicToReturn.size_hint = [1, None]
        GraphicToReturn.height = "70dp"

        # Add the button with its canvas at base
        GraphicToReturn.add_widget(cst_item.EmptyTransactionButton(size_x = textsize))

        # Add AssetName label - First initialize the dict
        label_params = {}
        label_params.update({'text_size': [textsize, None]})
        label_params.update({'pos_hint': {'x' : 0.5, 'y': 0}})
        label_params.update({'text': 'EMPTY'})
        label_params.update({'font_name': 'Candarab'})
        label_params.update({'font_size': 20})
        label_params.update({'color': [1,1,1,1]})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Return relative layout
        return GraphicToReturn

    # Define the transaction in input at the Box Layout
    def DefineFullTransaction(self, textsize, asset, TransactionDict, Index, Currency):
        self.TransactionDictIndex = Index

         # Get the necessary information from the AssetDictionary
        GraphicToReturn = RelativeLayout()
        GraphicToReturn.size_hint = [1, None]
        GraphicToReturn.height = "80dp"

        BoxLayoutToAdd = BoxLayout()
        BoxLayoutToAdd.size_hint = [1, None]
        BoxLayoutToAdd.height = "80dp"
        BoxLayoutToAdd.orientation = "horizontal"
        

        # Add the button with its canvas at base
        GraphicToReturn.add_widget(cst_item.TransactionButton(size_x = textsize, height = GraphicToReturn.height))

        # Add Date
        label_params = {}
        label_params.update({'text_size': [textsize, None]})
        label_params.update({'pos_hint': {'x' : 0.05, 'y': 0.2}})
        label_params.update({'text': TransactionDict['Date'] })
        label_params.update({'font_name': 'Candarab'})
        label_params.update({'font_size': 25})
        label_params.update({'color': [1,1,1,1]})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Amount
        label_params.update({'pos_hint': {'x' : 0.05, 'y': -0.2}})
        label_params.update({'text': str(TransactionDict['Amount']) + Currency})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Description
        label_params.update({'pos_hint': {'x' : 0.25, 'y': 0}})
        label_params.update({'text': TransactionDict['Note']})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Category
        label_params.update({'pos_hint': {'x' : 0.4, 'y': 0}})
        label_params.update({'text': TransactionDict['Category'] })
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Paid with
        label_params.update({'pos_hint': {'x' : 0.55, 'y': 0}})
        label_params.update({'text': str(TransactionDict['Paid with'])})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # # Define remove button
        Btn_size = [GraphicToReturn.size[0]/2.5, GraphicToReturn.size[1]/2.5]
        box_pos_hint = {'x' : 0.9, 'y': 0.5 - (Btn_size[1]/(2*GraphicToReturn.size[1])) }

        ModifyPopup = TransInOut_Popup.AddTransactionInOutPopup(title_str = 'MODIFY TRANSACTION ' + self.portfolio, type = 'M', PortfolioName = self.portfolio, Database = self.DBManager, ItemToMod = {self.TransactionDictIndex: TransactionDict})
        RemovePopup = RemoveTransactionInOutPopup.RemoveTransactionInOutPopup(title_str = 'REMOVE TRANSACTION', PortfolioName = self.portfolio, AssetName = asset, TransactionIndex = Index, DBManager = self.DBManager, ManagerOfScreen = self )

        Box = cst_item.ModifyRemoveButtonBox(Btn_size = Btn_size, box_pos_hint = box_pos_hint, ModifyPopup = ModifyPopup, RemovePopup = RemovePopup)
        GraphicToReturn.add_widget(Box)

        # Return relative layout
        return GraphicToReturn
                 

    # At the "Add Transaction" or Modify Transaction 
    def OpenAddTransactionPopup(self):
        # Define Popup and open it
        Popup = TransInOut_Popup.AddTransactionInOutPopup(title_str = 'ADD TRANSACTION ' + self.portfolio, type = 'A', PortfolioName = self.portfolio, Database = self.DBManager)
        Popup.open()

    ####################
    # MOVE SCREEN BACK #
    ####################
    def ReturnBack(self):
        ScreenManager = self.parent
        ScreenManager.current = 'TRANSACTION'
        ScreenManager.current_screen.UpdateScreen()