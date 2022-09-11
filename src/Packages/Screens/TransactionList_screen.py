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
        self.ids.TransactionListLabel.text = 'TRANSACTION ' + portfolio.upper()
        self.DBManager = Database
        self.portfolio = portfolio
        self.portfolio_list = portfolio + '_LIST'

        # Update Screen
        self.UpdateListOfTransaction()

    # Update the list of transaction given the portafolio name
    def UpdateListOfTransaction(self):
        json_file = self.DBManager.ReadJson()

        self.ids[self.ScreenToUpdate].clear_widgets()

        self.ids[self.ScreenToUpdate].add_widget(TransactionInOutLineSeparator())
        self.ids[self.ScreenToUpdate].add_widget(TransactionInOutRowBoxLayout_Title())

        for transaction_idx in json_file[self.portfolio_list]['Assets']['Transactions']['Transactions'].keys():
            self.ids[self.ScreenToUpdate].add_widget(TransactionInOutLineSeparator())
            # Extract the transaction to show
            transaction = json_file[self.portfolio_list]['Assets']['Transactions']['Transactions'][transaction_idx]
            
            # Append to the transaction list
            transaction.update({'TransactionNumber': str(transaction_idx)})
            self.ids[self.ScreenToUpdate].add_widget(TransactionInOutRowBoxLayout(transaction))

        # Add final separator
        self.ids[self.ScreenToUpdate].add_widget(TransactionInOutLineSeparator())

        # Add empty item to the widget
        if not len(self.ids[self.ScreenToUpdate].children): self.ids[self.ScreenToUpdate].add_widget(TransactionInOutRowBoxLayout_Empty)
                
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