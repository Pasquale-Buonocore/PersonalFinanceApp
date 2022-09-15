from Packages.CustomFunction.CustomFunction import ReturnJsonPathGivenScreenName
from Packages.CustomFunction.AssetDistributionGraph import AssetDistributionGraph
from Packages.CustomFunction.DefineJsonDatapath import return_updated_data_path
import Packages.CustomItem.Popup.RemoveAssetPopup as RemoveAssetPopup
import Packages.CustomItem.Popup.AddAssetPopup as AddAssetPopup
from Packages.CustomItem.Lists.AssetListManagement import *
import Packages.DatabaseMng.PortfolioManager as db_manager
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
import Packages.CustomItem.Popup.RemovingPopup as Rm_popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

class AssetsScreen(Screen):
    def __init__(self, **kwargs):
        # Call superclass
        super().__init__(**kwargs)
        # Graphic element which will be updated time by time
        self.ScreenToUpdate = 'AssetsHeader'

    #########################
    #    UPDATE FUNCTION    #
    #########################

    # Function to call tu update the Asset screen
    def UpdateScreen(self, FromScreenName, PortfolioName, PortfolioCurrency):
        # Save the father name
        self.FromScreenName = FromScreenName # contains the screen from which the assets screen has been opened 
        self.PortfolioName = PortfolioName # contains the portfolio that has been clicked in the FromScreen
        self.PortfolioCurrency = PortfolioCurrency
        self.PortfolioJsonPath = ReturnJsonPathGivenScreenName(self.FromScreenName)
        self.DBManager = db_manager.PortfoliosManager_Class(return_updated_data_path(PathManager_Class.database_path), self.PortfolioJsonPath)

        # Update the Label of the String
        self.ids['DashboardTitle'].text = 'DASHBOARD - ASSET IN PORTFOLIO ' + self.PortfolioName.upper() + ' [' + self.FromScreenName.upper() + ']'

        # Update graphic elements
        self.UpdateListOfAssets()

        # Update allocation
        self.DBManager.UpdatePortfolioDesiredAssetAllocation(self.PortfolioName)
        self.DBManager.UpdatePortfolioActualAssetAllocation(self.PortfolioName)

        # Update graph and load it
        color = self.UpdateGraph()
        self.ids.GraphImage.source = 'images/Support/AssetsInPortfolio.png'
        self.ids.GraphImage.reload()

        # Update table of allocation
        self.UpdateAssetAllocationTable(color = color)

    # Function to call when "Back" button is pressed
    def ReturnBack(self):
        print('Returnig back to ' + self.FromScreenName)
        self.parent.current = 'PORTFOLIO'
        self.parent.current_screen.UpdateScreen(ScreenName = self.FromScreenName, PortfolioJsonPath = ReturnJsonPathGivenScreenName(self.FromScreenName))
    
    #####################
    #    ASSETS  BOX    #
    #####################

    # Fill the Box Layout in Crypto Screen with a list of portfolios
    def UpdateListOfAssets(self):
        self.DBManager.UpdateAllAssetStatistics(self.PortfolioName)

        # Clear the Item inside the BoxLayout (Keep the first element only)
        self.ids[self.ScreenToUpdate].clear_widgets()

        self.ids[self.ScreenToUpdate].add_widget(AssetLineSeparator())
        self.ids[self.ScreenToUpdate].add_widget(AssetRowBoxLayout_Title())

        Assets_json = self.DBManager.ReadJson()[self.PortfolioName]['Assets']
        Currency_str = self.DBManager.ReadJson()[self.PortfolioName]['Statistics']['Currency']


        if len(Assets_json.keys()):
            # Add an item for each portfolio
            for asset in Assets_json.keys():
                # Compute the graphic element to Add given the PortfolioName and its statistics
                self.ids[self.ScreenToUpdate].add_widget(AssetLineSeparator())

                RelLayout = RelativeLayout()
                RelLayout.size_hint = [1, None]
                RelLayout.height = MDApp.get_running_app().Configuration_DB.GetElementValue('AssetRowBoxLayoutHeight')
                RelLayout.add_widget(AssetRowButton())
                AssetProperties = Assets_json[asset]['Statistics']
                AssetProperties.update({'AssetName' : asset})
                AssetProperties.update({'Currency' : Currency_str})
                RelLayout.add_widget(AssetRowBoxLayout(Properties = AssetProperties))
                
                self.ids[self.ScreenToUpdate].add_widget(RelLayout)
            
            # Append the last line
            self.ids[self.ScreenToUpdate].add_widget(AssetLineSeparator())
        else:
            # Add empty item
            self.ids[self.ScreenToUpdate].add_widget(AssetRowBoxLayout_Empty())

    # When the Add New Asset button is pressed
    def AddNewAssetPopup(self):
        print('Add new asset Popup')
        # Initialize the popup
        AddAssetPop = AddAssetPopup.AddAssetPopup(title_str = 'ADD NEW ASSET', type = 'A', Database = self.DBManager, PortfolioName = self.PortfolioName)
        # Open the Popup
        AddAssetPop.open()

    #######################
    #    DASHBOARD BOX    #
    #######################

    def OpenAssetTransactionScreen(self, AssetName):
        self.parent.current = 'ASSETS TRANSACTION'
        self.parent.current_screen.UpdateScreen(AssetName = AssetName, PortfolioName = self.PortfolioName, PortfolioCurrency = self.PortfolioCurrency, FromScreenName = self.FromScreenName)

    # The function generates a picture of the allocation, which is the loaded in the GUI
    def UpdateGraph(self):
        JsonFile = self.DBManager.ReadJson()

        ListOfAssets = list(JsonFile[self.PortfolioName]['Assets'].keys())
        ListOfAssetsValue = []

        for Asset in ListOfAssets:
            ListOfAssetsValue.append(JsonFile[self.PortfolioName]['Assets'][Asset]['Statistics']['TotalValue'])

        # Update image
        return AssetDistributionGraph(ListOfAssets, ListOfAssetsValue, 'AssetsInPortfolio')

    # The function updates the allocation table to compare the two allocation.
    # Future allocation will allow the user to reallocate with or without additional capital
    def UpdateAssetAllocationTable(self, color):
        # AssetAllocationTable is the box whose children are the row of the table
        Json_File = self.DBManager.ReadJson()

        # Clear widget of BoxLayout
        self.ids.AssetAllocationTable.clear_widgets()

        # Define color for legend
        ColorIndex = list(color.keys())
        ColorIndex.reverse()

        for asset in Json_File[self.PortfolioName]['Assets'].keys():
            # 1. AssetName, 2. DesiredAllocation, 3. ActualAllocation (Green if bigger, Red if lesser)

            Box = BoxLayout(orientation = 'horizontal', size_hint = [1, None], height = "20dp")

            # Graphic Color
            ColoredCircle = Button(pos_hint = {'x': 0.5, 'y' : 0}, size_hint = [0.05, None], height = '20dp', background_color = color[ColorIndex.pop()], text = '')

            # Asset Label
            AssetLabel = Label(size_hint = [0.35, None], text = asset)
            AssetLabel.text_size = [AssetLabel.width, None]
            AssetLabel.size = AssetLabel.texture_size 
            AssetLabel.height = "20dp"
            AssetLabel.halign = 'center'

            # Asset desired allocation Label
            DesiredAllocationLabel = Label(size_hint = [0.3, None], text = str(Json_File[self.PortfolioName]['Statistics']['DesiredAssetAllocation'][asset]) + "%")
            DesiredAllocationLabel.text_size = [DesiredAllocationLabel.width, None]
            DesiredAllocationLabel.size = DesiredAllocationLabel.texture_size 
            DesiredAllocationLabel.height = "20dp"
            DesiredAllocationLabel.halign = 'center'

            # Asset Actual allocation Label
            ActualAllocationLabel = Label(size_hint = [0.3, None], text = str(Json_File[self.PortfolioName]['Statistics']['ActualAssetAllocation'][asset]) + "%")
            ActualAllocationLabel.text_size = [ActualAllocationLabel.width, None]
            ActualAllocationLabel.size = ActualAllocationLabel.texture_size 
            ActualAllocationLabel.height = "20dp"
            ActualAllocationLabel.halign = 'center'
    
            Box.add_widget(ColoredCircle)
            Box.add_widget(AssetLabel)
            Box.add_widget(DesiredAllocationLabel)
            Box.add_widget(ActualAllocationLabel)

            self.ids.AssetAllocationTable.add_widget(Box)

        
