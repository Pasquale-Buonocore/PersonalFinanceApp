import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.CustomPopup as cst_popup
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

class CryptoScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Initialize the manager of the json manager
        self.DBManager = db_manager.PortfoliosManager_Class(db_manager.path_manager.database_path,db_manager.path_manager.Crypto_path)
        self.ScreenToUpdate = 'PortfolioHeader'

    def UpdateScreen(self):
        self.UpdateListOfPortfolio()
        pass

    #####################
    #    CRYPTO  BOX    #
    #####################

    # Fill the Box Layout in Crypto Screen with a list of portfolios
    def UpdateListOfPortfolio(self):
        print('ciao')
        # Store the first Item containing the screen name
        First_widget = self.ids[self.ScreenToUpdate].children[-1]

        # Store the BoxLayout containg the portfolios Relative layout
        Second_widget = self.ids[self.ScreenToUpdate].children[-2]
        Second_widget.clear_widgets()
        
        # Clear the Item inside the BoxLayout (Keep the first element only)
        self.ids[self.ScreenToUpdate].clear_widgets()

        # Add the first and second item again
        self.ids[self.ScreenToUpdate].add_widget(First_widget)
        self.ids[self.ScreenToUpdate].add_widget(Second_widget)

        # Then, for each portfolio in the json add a New Portfolio in the self.ids[self.ScreenToUpdate]
        Portfolios_json = self.DBManager.ReadJson()

        # Size dello ScreenManager
        ScreenManagerSize_x = self.parent.size[0]
        BoxLayoutPadding_ls= self.children[0].children[0].padding[0]
        BoxLayoutPadding_rs = self.children[0].children[0].padding[2]
    
        text_size = ScreenManagerSize_x - BoxLayoutPadding_ls - BoxLayoutPadding_rs

        for portfolio in Portfolios_json.keys():
            # Compute the graphic element to Add given the PortfolioName and its statistics
            self.ids[self.ScreenToUpdate].children[-2].add_widget(self.DefineCryptoPortfolio(PortfolioName = portfolio, PortfolioDict_Stats = Portfolios_json[portfolio]['Statistics'], textsize = text_size))

    # Define the Portfolio given in input a dictionary 
    def DefineCryptoPortfolio(self, PortfolioName = '', PortfolioDict_Stats = {}, textsize = 0):
        # Get the necessary information from the PortfolioDictionary
        GraphicToReturn = RelativeLayout()
        GraphicToReturn.size_hint = [1, None]
        GraphicToReturn.height = "120dp"
        GraphicToReturn.id = PortfolioName

        # Add the button with its canvas at base
        GraphicToReturn.add_widget(cst_item.PortfolioButton(size_x = textsize))

        # Add PortfolioName label - First initialize the dict
        label_params = {}
        label_params.update({'text_size': [textsize, None]})
        label_params.update({'pos_hint': {'x' : 0.025, 'y': 0.2}})
        label_params.update({'text': 'PORTFOLIO NAME'})
        label_params.update({'font_name': 'Candarab'})
        label_params.update({'font_size': 20})
        label_params.update({'color': [1,1,1,1]})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Add PortfolioName str
        label_params.update({'pos_hint': {'x' : 0.025, 'y': -0.2}})
        label_params.update({'text': PortfolioName})
        label_params.update({'font_size': 35})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Add Portfolio Value Lbl
        label_params.update({'pos_hint': {'x' : 0.3, 'y': 0.2}})
        label_params.update({'text': 'PORTFOLIO VALUE'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Add Portfolio Value
        label_params.update({'pos_hint': {'x' : 0.3, 'y': -0.2}})
        label_params.update({'text': str(PortfolioDict_Stats['TotalValue']) + str(PortfolioDict_Stats['Currency'])})
        label_params.update({'font_size': 35})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Add Portfolio Asset Lbl
        label_params.update({'pos_hint': {'x' : 0.5, 'y': 0.2}})
        label_params.update({'text': 'NUMBER OF ASSET'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Add Portfolio Asset
        label_params.update({'pos_hint': {'x' : 0.5, 'y': -0.2}})
        label_params.update({'text': str(PortfolioDict_Stats['NumberOfAssets'])})
        label_params.update({'font_size': 35})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Add Portfolio Status lbl
        label_params.update({'pos_hint': {'x' : 0.7, 'y': 0.2}})
        label_params.update({'text': 'RESUME STATUS'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Add Portfolio Asset
        color = [0,1,0,1] if PortfolioDict_Stats['TotalProfit'] >= 0 else [1,0,0,1]
        label_params.update({'pos_hint': {'x' : 0.7, 'y': -0.2}})
        label_params.update({'text': str(PortfolioDict_Stats['TotalProfit']) + str(PortfolioDict_Stats['Currency'])})
        label_params.update({'font_size': 35})
        label_params.update({'color': color})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Define remove button
        Btn_size = [GraphicToReturn.size[0]/2.5, GraphicToReturn.size[1]/2.5]
        box_pos_hint = {'x' : 0.9, 'y': 0.5 - (Btn_size[1]/(2*GraphicToReturn.size[1])) }
        Box = cst_item.ModifyRemoveButtonBox(Btn_size = Btn_size, box_pos_hint = box_pos_hint)
        GraphicToReturn.add_widget(Box)

        # Return relative layout
        return GraphicToReturn


    ###################
    # ASSE ALLOCATION #
    ###################

