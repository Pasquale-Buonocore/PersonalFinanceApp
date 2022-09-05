import Packages.CustomItem.Popup.RemovePortfolioPopup as RemovePortfolioPopup
import Packages.CustomItem.Popup.AddPortfolioPopup as AddPortfolioPopup
from Packages.CustomItem.Lists.PortfolioListManagement import *
import Packages.DatabaseMng.PortfolioManager as db_manager
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

class PortfolioScreen(Screen):
    def __init__(self, ScreenName = 'CRYPTO', PortfolioJsonPath = db_manager.path_manager.Crypto_path , **kwargs):
        # Call superclass
        super().__init__(**kwargs)
        # Graphic element which will be updated time by time
        self.ScreenToUpdate = 'PortfolioHeader'
        
        # Initialize the manager of the json manager
        self.UpdateInternalData(ScreenName, PortfolioJsonPath)
        
    #########################
    #    UPDATE FUNCTION    #
    #########################

    def UpdateScreen(self, ScreenName, PortfolioJsonPath):
        self.UpdateInternalData(ScreenName = ScreenName, PortfolioJsonPath = PortfolioJsonPath)

        # Update graphic elements 
        self.ids.FirstRowName.text = ScreenName + ' - PORTFOLIO LIST'

        # Update list of portfolio
        self.UpdateListOfPortfolio()

    def UpdateInternalData(self, ScreenName, PortfolioJsonPath):
        # Update signals
        self.ScreenName = ScreenName
        self.PortfolioJsonPath = PortfolioJsonPath
        self.DBManager = db_manager.PortfoliosManager_Class(db_manager.path_manager.database_path, self.PortfolioJsonPath)

    ########################
    #    PORTFOLIO  BOX    #
    ########################

    # Fill the Box Layout in Portfolio Screen with a list of portfolios
    def UpdateListOfPortfolio(self):
        self.DBManager.UpdateAllPortfolioStatistics()

        # Clear the Item inside the BoxLayout (Keep the first element only)
        self.ids[self.ScreenToUpdate].clear_widgets()
        
        self.ids[self.ScreenToUpdate].add_widget(PortfolioLineSeparator())
        self.ids[self.ScreenToUpdate].add_widget(PortfolioRowBoxLayout_Title())
        
        # Then, for each portfolio in the json add a New Portfolio in the self.ids[self.ScreenToUpdate]
        Portfolios_json = self.DBManager.ReadJson()
        
        # If there are portfolios defined for such category, populate it
        if len(Portfolios_json.keys()):
            for portfolio in Portfolios_json.keys():
                # Compute the graphic element to Add given the PortfolioName and its statistics
                self.ids[self.ScreenToUpdate].add_widget(PortfolioLineSeparator())

                RelLayout = RelativeLayout()
                RelLayout.size_hint = [1, None]
                RelLayout.height = MDApp.get_running_app().Configuration.GetElementValue('PortfolioRowBoxLayoutHeight')
                RelLayout.add_widget(PortfolioRowButton())
                PortfolioProperties = Portfolios_json[portfolio]['Statistics']
                PortfolioProperties.update({'PortfolioName' : portfolio})
                RelLayout.add_widget(PortfolioRowBoxLayout(Properties = PortfolioProperties))
                
                self.ids[self.ScreenToUpdate].add_widget(RelLayout)
            
            # Close with a final separator
            self.ids[self.ScreenToUpdate].add_widget(PortfolioLineSeparator())
        # else, show that the portfolio is empty
        else:
            self.ids[self.ScreenToUpdate].add_widget(PortfolioLineSeparator())
            self.ids[self.ScreenToUpdate].add_widget(PortfolioRowBoxLayout_Empty())

    def OpenAssetPortfolioScreen(self, PortfolioName):
        self.parent.current = 'ASSETS'
        self.parent.current_screen.UpdateScreen(FromScreenName = self.ScreenName, PortfolioName = PortfolioName)

    # When the Add New Portfolio button is pressed
    def AddNewPortfolioPopup(self):
        print('Add new Portfolio')
        # Initialize the popup
        AddPortfolioPop = AddPortfolioPopup.AddPortfolioPopup(title_str = 'ADD NEW PORTFOLIO', type = 'A')
        # Open the Popup
        AddPortfolioPop.open()

