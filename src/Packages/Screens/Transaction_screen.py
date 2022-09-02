from Packages.CustomFunction.AssetDistributionGraph import AssetDistributionGraph
import Packages.CustomItem.Popup.TransactionCategoryListPopup as trans_popup
import Packages.DatabaseMng.PortfolioManager as db_manager
import Packages.DatabaseMng.PathManager as path_manager
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class TransactionScreen(Screen):
    def __init__(self,**kwargs):
        # Initialize super class
        super().__init__(**kwargs)

        # Initialize the manager of the json manager
        self.TransactionIn = db_manager.PortfoliosManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.TransactionIn_path)
        self.TransactionOut = db_manager.PortfoliosManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.TransactionOut_path)
        self.Image_path_manager = path_manager.PathImage_Class()
        self.CheckTransactionPortfolio(Database = self.TransactionIn, Name = "IN")
        self.CheckTransactionPortfolio(Database = self.TransactionOut, Name = "OUT")

        # Define portfolios images name
        self.TransactionInImagePath = self.Image_path_manager.TransactionIn_imagepath
        self.TransactionOutImagePath = self.Image_path_manager.TransactionOut_imagepath

    def UpdateScreen(self):
        # Update statistics for all portfolios
        self.TransactionIn.UpdateTransactionPortfolio("IN")
        self.TransactionOut.UpdateTransactionPortfolio("OUT")

        # Update graph for output and inpuy transaction
        self.color_list_IN = self.UpdateGraphs({"IN" : self.TransactionIn.ReadJson()["IN"]}, self.TransactionInImagePath)
        self.color_list_OUT = self.UpdateGraphs({ "OUT" : self.TransactionOut.ReadJson()["OUT"]}, self.TransactionOutImagePath)

        # Assign the correct image of graphs
        self.ids.GraphTransactionIn.source = self.Image_path_manager.image_basepath + self.Image_path_manager.TransactionIn_imagepath + '.png'
        self.ids.GraphTransactionOut.source = self.Image_path_manager.image_basepath + self.Image_path_manager.TransactionOut_imagepath + '.png'

        # Update graphs
        self.ids.GraphTransactionOut.reload()
        self.ids.GraphTransactionIn.reload()

        # Update tables
        # self.UpdateAssetAllocationTable(color_list = [self.color_list_IN, self.color_list_OUT])

    ####################
    # CLASS MANAGEMENT #
    ####################

    # Check if portfolios "TRANSACTION IN" and  "TRANSACTION OUT" exist in the database
    def CheckTransactionPortfolio(self, Database, Name):
        # Define boolean
        Is_present = False
        LIST_is_present = False

        for PortfolioName in Database.ReadJson().keys():
            # Check if it is the portfolio whose entry are the caterogy of transaction
            if PortfolioName == Name: Is_present = True
            # Check if it is the portfolio whose entry are the transaction
            elif PortfolioName == (Name + "_LIST"): LIST_is_present = True
            # Otherwise remove it
            else: Database.RemovePortfolio(PortfolioName)

        if not Is_present: Database.AddPortfolio(Database.InitializeTransactionPortfolio(Name, ['€', 0]))
        if not LIST_is_present: Database.AddPortfolio(Database.InitializeTransactionListPortfolio(Name + "_LIST"))

    # Move to the transaction list
    def MoveToTransactionScreen(self, direction = 'IN', Database = {}):
        ScreenManager = self.parent
        ScreenManager.current = 'TRANSACTION LIST'
        ScreenManager.current_screen.UpdateScreen(portfolio = direction, Database = Database)

    # Open to popup which allows to see and modify the class of transaction
    def ModifyCategory(self, type = 'IN', Database = ''):
        # Open the popup that will allow to Modify the category      
        ModifyClassesPopup = trans_popup.TransactionCategoryListPopup(transaction_type = type, DBManager = Database)
        ModifyClassesPopup.open()

    # Updates graph
    def UpdateGraphs(self, Portfolio, Image_path):
        color_list = []

        # Update transaction In graph
        for type in Portfolio.keys():
            ListOfAssetsPass = list(Portfolio[type]['Assets'].keys())
            ListOfAssetValuePass = []

            for Asset in ListOfAssetsPass:
                ListOfAssetValuePass.append(Portfolio[type]['Assets'][Asset]['Statistics']['TotalValue'])

            color_list.append(AssetDistributionGraph(ListOfAssets = ListOfAssetsPass, ListOfAssetValue = ListOfAssetValuePass, image_name = Image_path))

        # return color of the graphs
        return color_list

    # The function updates the allocation table to compare the two allocation for both Transaction In and Transaction Out
    def UpdateAssetAllocationTable(self, color_list):
        # AssetAllocationTable is the box whose children are the row of the table
        Json_File = self.DBManager.ReadJson()

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