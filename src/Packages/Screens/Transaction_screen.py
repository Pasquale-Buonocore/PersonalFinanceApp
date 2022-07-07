from Packages.CustomFunction.AssetDistributionGraph import AssetDistributionGraph
import Packages.CustomItem.TransactionCategoryListPopup as trans_popup
import Packages.DatabaseMng.PortfolioManager as db_manager
import Packages.DatabaseMng.PathManager as path_manager
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.CustomItem.RemovingPopup as Rm_popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class TransactionScreen(Screen):
    def __init__(self,**kwargs):
        # Initialize super class
        super().__init__(**kwargs)

        # Initialize the manager of the json manager
        self.Transaction_DBManager = db_manager.PortfoliosManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Transaction_path)
        self.Image_path_manager = path_manager.PathImage_Class()
        self.CheckTransactionPortfolio()

        # Define portfolios images name
        self.TransactionInImagePath = self.Image_path_manager.TransactionIn_imagepath
        self.TransactionOutImagePath = self.Image_path_manager.TransactionOut_imagepath


    def UpdateScreen(self):

        # Update graph for output and inpuy transaction
        self.UpdateGraphs()

        # Assign the correct image of graphs
        self.ids.GraphTransactionOut.source = self.Image_path_manager.image_basepath + self.Image_path_manager.TransactionIn_imagepath + '.png'
        self.ids.GraphTransactionIn.source = self.Image_path_manager.image_basepath + self.Image_path_manager.TransactionOut_imagepath + '.png'

        # Update graphs
        self.ids.GraphTransactionOut.reload()
        self.ids.GraphTransactionIn.reload()

    ####################
    # CLASS MANAGEMENT #
    ####################

    # Check if portfolios "TRANSACTION IN" and  "TRANSACTION OUT" exist in the database
    def CheckTransactionPortfolio(self):
        # Future update will consider the possibility to have multiple transaction portfolio
        for PortfolioName in ["IN", "OUT"]:
            if PortfolioName not in self.Transaction_DBManager.ReadJson().keys():
                NewPftl = self.Transaction_DBManager.InitializeTransactionPortfolio(PortfolioName, ['€', 0])
                self.Transaction_DBManager.AddPortfolio(NewPftl)

    # Move to the transaction list
    def MoveToTransactionScreen(self, type = 'IN'):
        ScreenManager = self.parent
        ScreenManager.current = 'TRANSACTION LIST'
        ScreenManager.current_screen.UpdateScreen(type = type)

    # Open to popup which allows to see and modify the class of transaction
    def ModifyCategory(self, type = 'IN'):
        # Open the popup that will allow to Modify the category
        ModifyClassesPopup = trans_popup.TransactionCategoryListPopup(type)
        ModifyClassesPopup.open()

    def UpdateGraphs(self):
        Portfolios = self.Transaction_DBManager.ReadJson()
        color_list = []
        Image_path_list = [self.TransactionOutImagePath, self.TransactionInImagePath]

        # Update transaction In graph
        for type in Portfolios.keys():
            ListOfAssetsPass = list(Portfolios[type]['Assets'].keys())
            ListOfAssetValuePass = []

            for Asset in ListOfAssetsPass:
                ListOfAssetValuePass.append(Portfolios[type]['Assets'][Asset]['Statistics']['TotalAmount'])

            color_list.append(AssetDistributionGraph(ListOfAssets = ListOfAssetsPass, ListOfAssetValue = ListOfAssetValuePass, image_name = Image_path_list.pop()))


        # return color of the graphs
        return color_list
