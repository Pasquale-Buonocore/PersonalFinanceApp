import Packages.CustomItem.Popup.RemoveTransactionInOutPopup as RemoveTransactionInOutPopup
import Packages.CustomItem.Popup.AddTransactionInOutPopup as TransInOut_Popup
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.CustomItem.Lists.TransactionInOutListManagement import *
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout


class TransactionListScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        # Store info of the Box Layout to fill in
        self.ScreenToUpdate = 'TransactionListBoxLayout'
    
    # Function to call when moving towards that page
    def UpdateScreen(self, portfolio, Database):
        self.Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
        self.ids.TransactionListLabel.text = 'TRANSACTION ' + portfolio.upper()
        self.DBManager = Database
        self.portfolio = portfolio

        # Update Screen
        self.UpdateListOfTransaction()

    # Update the list of transaction given the portafolio name
    def UpdateListOfTransaction(self):
        return
        json_file = self.DBManager.ReadJson()

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
                

    ####################
    # MOVE SCREEN BACK #
    ####################

    # At the "Add Transaction" or Modify Transaction 
    def OpenAddTransactionPopup(self):
        # Define Popup and open it
        Popup = TransInOut_Popup.AddTransactionInOutPopup(title_str = 'ADD TRANSACTION ' + self.portfolio, type = 'A', PortfolioName = self.portfolio, Database = self.DBManager)
        Popup.open()

    def ReturnBack(self):
        ScreenManager = self.parent
        ScreenManager.current = 'TRANSACTION'
        ScreenManager.current_screen.UpdateScreen()