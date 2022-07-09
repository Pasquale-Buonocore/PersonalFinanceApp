from Packages.CustomFunction.AssetDistributionGraph import AssetDistributionGraph
import Packages.CustomItem.TransactionCategoryListPopup as trans_popup
import Packages.DatabaseMng.PortfolioManager as db_manager
import Packages.DatabaseMng.PathManager as path_manager
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.CustomItem.RemovingPopup as Rm_popup
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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
        # Update statistics for all portfolios
        self.Transaction_DBManager.UpdateAllTransactionPortfolioStatistics()

        # Update graph for output and inpuy transaction
        color_list = self.UpdateGraphs()

        # Assign the correct image of graphs
        self.ids.GraphTransactionIn.source = self.Image_path_manager.image_basepath + self.Image_path_manager.TransactionIn_imagepath + '.png'
        self.ids.GraphTransactionOut.source = self.Image_path_manager.image_basepath + self.Image_path_manager.TransactionOut_imagepath + '.png'

        # Update graphs
        self.ids.GraphTransactionOut.reload()
        self.ids.GraphTransactionIn.reload()

        # Update tables
        self.UpdateAssetAllocationTable(color_list = color_list)

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
    def MoveToTransactionScreen(self, direction = 'IN'):
        ScreenManager = self.parent
        ScreenManager.current = 'TRANSACTION LIST'
        ScreenManager.current_screen.UpdateScreen(portfolio = direction, Database = self.Transaction_DBManager)

    # Open to popup which allows to see and modify the class of transaction
    def ModifyCategory(self, type = 'IN'):
        # Open the popup that will allow to Modify the category      
        ModifyClassesPopup = trans_popup.TransactionCategoryListPopup(type)
        ModifyClassesPopup.open()

    # Populate allocation tables
    def UpdateAllocationTables(self):
        pass

    # Updates graph
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

    # The function updates the allocation table to compare the two allocation for both Transaction In and Transaction Out
    def UpdateAssetAllocationTable(self, color_list):
        # AssetAllocationTable is the box whose children are the row of the table
        Json_File = self.Transaction_DBManager.ReadJson()

        ColorToAppend = {'IN': color_list[0], 'OUT' : color_list[1]}
        TableToAppend = {'IN': 'TransactionInTable', 'OUT' : 'TransactionOutTable'}

        for portfolio in Json_File.keys():
            # Clear widget of BoxLayout
            self.ids[TableToAppend[portfolio]].clear_widgets()

            # Define color for legend
            ColorIndex = list(ColorToAppend[portfolio].keys())
            ColorIndex.reverse()

            for asset in Json_File[portfolio]['Assets'].keys():
                # 1. AssetName, 2. DesiredAllocation, 3. ActualAllocation (Green if bigger, Red if lesser)

                Box = BoxLayout(orientation = 'horizontal', size_hint = [1, None], height = "20dp")

                # Graphic Color
                ColoredCircle = Button(pos_hint = {'x': 0.5, 'y' : 0}, size_hint = [0.05, None], height = '20dp', background_color = ColorToAppend[portfolio][ColorIndex.pop()], text = '')

                # Asset Label
                AssetLabel = Label(size_hint = [0.35, None], text = asset)
                AssetLabel.text_size = [AssetLabel.width, None]
                AssetLabel.size = AssetLabel.texture_size 
                AssetLabel.height = "20dp"
                AssetLabel.halign = 'center'

                # Asset desired allocation Label
                DesiredAllocationLabel = Label(size_hint = [0.3, None], text = str(Json_File[portfolio]['Statistics']['DesiredAssetAllocation'][asset]) + '€')
                DesiredAllocationLabel.text_size = [DesiredAllocationLabel.width, None]
                DesiredAllocationLabel.size = DesiredAllocationLabel.texture_size 
                DesiredAllocationLabel.height = "20dp"
                DesiredAllocationLabel.halign = 'center'

                # Asset Actual allocation Label
                ActualAllocationLabel = Label(size_hint = [0.3, None], text = str(Json_File[portfolio]['Statistics']['ActualAssetAllocation'][asset]) + "€")
                ActualAllocationLabel.text_size = [ActualAllocationLabel.width, None]
                ActualAllocationLabel.size = ActualAllocationLabel.texture_size 
                ActualAllocationLabel.height = "20dp"
                ActualAllocationLabel.halign = 'center'
    
                Box.add_widget(ColoredCircle)
                Box.add_widget(AssetLabel)
                Box.add_widget(DesiredAllocationLabel)
                Box.add_widget(ActualAllocationLabel)

                self.ids[TableToAppend[portfolio]].add_widget(Box)