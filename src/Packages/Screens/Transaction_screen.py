import Packages.DatabaseMng.JsonManagerList as jsonList_manager
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
        self.TransactionIn_DBManager = jsonList_manager.JsonManagerList_Class(jsonList_manager.path_manager.database_path,jsonList_manager.path_manager.TransactionIn_path)
        self.TransactionOut_DBManager = jsonList_manager.JsonManagerList_Class(jsonList_manager.path_manager.database_path,jsonList_manager.path_manager.TransactionOut_path)

    def UpdateScreen(self):

        # Update graph for output transaction
        self.ids.GraphTransactionOut.source = 'images/Support/AssetsInPortfolio.png'
        self.ids.GraphTransactionOut.reload()

        # Update graph for input transaction
        self.ids.GraphTransactionIn.source = 'images/Support/AssetsInPortfolio.png'
        self.ids.GraphTransactionIn.reload()

    def MoveToTransactionScreen(self, type = 'IN'):

        # Update Screen
        ScreenManager = self.parent
        ScreenManager.current = 'TRANSACTION LIST'
        ScreenManager.current_screen.UpdateScreen(type = type)
