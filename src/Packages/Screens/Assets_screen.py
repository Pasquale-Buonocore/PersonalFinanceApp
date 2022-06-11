from Packages.CustomFunction.CustomFunction import ReturnJsonPathGivenScreenName
import Packages.CustomItem.RemoveAssetPopup as RemoveAssetPopup
import Packages.CustomItem.AddAssetPopup as AddAssetPopup
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.DatabaseMng.DatabaseMng as db_manager
import Packages.CustomItem.RemovingPopup as Rm_popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen

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
    def UpdateScreen(self, FromScreenName, PortfolioName):
        # Save the father name
        self.FromScreenName = FromScreenName # contains the screen from which the assets screen has been opened 
        self.PortfolioName = PortfolioName # contains the portfolio that has been clicked in the FromScreen 
        self.PortfolioJsonPath = ReturnJsonPathGivenScreenName(self.FromScreenName)
        self.DBManager = db_manager.PortfoliosManager_Class(db_manager.path_manager.database_path, self.PortfolioJsonPath)
        
        # Update the Label of the String
        self.ids['FirstRowLabel'].text = 'ASSETS IN ' + self.PortfolioName.upper() + ' PORTFOLIO [' + self.FromScreenName.upper() + ']'

        # Update grahic elements
        self.UpdateListOfAssets()

    # Function to call when "Back" button is pressed
    def ReturnBack(self):
        print('Returnig back to ' + self.FromScreenName)
        ScreenManager = self.parent
        ScreenManager.current = 'PORTFOLIO'
        ScreenManager.current_screen.UpdateScreen(ScreenName = self.FromScreenName, PortfolioJsonPath = ReturnJsonPathGivenScreenName(self.FromScreenName))

    #####################
    #    ASSETS  BOX    #
    #####################

    # Fill the Box Layout in Crypto Screen with a list of portfolios
    def UpdateListOfAssets(self):
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
        Assets_json = self.DBManager.ReadJson()[self.PortfolioName]['Assets']
        Currency_str = self.DBManager.ReadJson()[self.PortfolioName]['Statistics']['Currency']

        # Size dello ScreenManager
        ScreenManagerSize_x = self.parent.size[0]
        BoxLayoutPadding_ls= self.children[0].children[0].padding[0]
        BoxLayoutPadding_rs = self.children[0].children[0].padding[2]
        text_size = ScreenManagerSize_x - BoxLayoutPadding_ls - BoxLayoutPadding_rs

        if len(Assets_json.keys()):
            # Add an item for each portfolio
            for asset in Assets_json.keys():
                # Compute the graphic element to Add given the AssetName and its statistics
                self.ids[self.ScreenToUpdate].children[-2].add_widget(self.DefineCryptoAsset(AssetName = asset, AssetDict_Stats = Assets_json[asset]['Statistics'], textsize = text_size, Currency = Currency_str))
        else:
            # Add empty item
            self.ids[self.ScreenToUpdate].children[-2].add_widget(self.DefineEmptyAsset(textsize = text_size))

    # Define an empty assets with the "EMPTY" label inside
    def DefineEmptyAsset(self, textsize = 0):
        # Get the necessary information from the AssetDictionary
        GraphicToReturn = RelativeLayout()
        GraphicToReturn.size_hint = [1, None]
        GraphicToReturn.height = "120dp"

        # Add the button with its canvas at base
        GraphicToReturn.add_widget(cst_item.EmptyPortfolioButton(size_x = textsize))

        # Add AssetName label - First initialize the dict
        label_params = {}
        label_params.update({'text_size': [textsize, None]})
        label_params.update({'pos_hint': {'x' : 0.5, 'y': 0}})
        label_params.update({'text': 'EMPTY'})
        label_params.update({'font_name': 'Candarab'})
        label_params.update({'font_size': 20})
        label_params.update({'color': [1,1,1,1]})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Return relative layout
        return GraphicToReturn

    # Define the asset given in input a dictionary 
    def DefineCryptoAsset(self, AssetName = '', AssetDict_Stats = {}, textsize = 0, Currency = '€'):
        # Get the necessary information from the AssetDictionary
        GraphicToReturn = RelativeLayout()
        GraphicToReturn.size_hint = [1, None]
        GraphicToReturn.height = "120dp"
        GraphicToReturn.id = AssetName

        # Add the button with its canvas at base
        GraphicToReturn.add_widget(cst_item.AssetButton(size_x = textsize, FromScreenName = self.FromScreenName, PortfolioName = self.PortfolioName, AssetName = AssetName))

        # Add AssetName label - First initialize the dict
        label_params = {}
        label_params.update({'text_size': [textsize, None]})
        label_params.update({'pos_hint': {'x' : 0.025, 'y': 0.2}})
        label_params.update({'text': 'ASSET NAME'})
        label_params.update({'font_name': 'Candarab'})
        label_params.update({'font_size': 20})
        label_params.update({'color': [1,1,1,1]})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # # Add AssetName str
        label_params.update({'pos_hint': {'x' : 0.025, 'y': -0.2}})
        label_params.update({'text': AssetName + ' [' + str(AssetDict_Stats['Symbol']) + ']'})
        label_params.update({'font_size': 23})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Quantity Asset Lbl
        label_params.update({'pos_hint': {'x' : 0.35, 'y': 0.2}})
        label_params.update({'text': 'CUR PRICE'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Quantity Value
        label_params.update({'pos_hint': {'x' : 0.35, 'y': -0.2}})
        label_params.update({'text': '0' + Currency})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Quantity Asset Lbl
        label_params.update({'pos_hint': {'x' : 0.45, 'y': 0.2}})
        label_params.update({'text': 'HOLDING'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Quantity Value
        label_params.update({'pos_hint': {'x' : 0.45, 'y': -0.2}})
        label_params.update({'text': str(AssetDict_Stats['Quantity'])})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Avarage Price lbl
        label_params.update({'pos_hint': {'x' : 0.55, 'y': 0.2}})
        label_params.update({'text': 'AVG PRICE'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Avarage Price Value
        label_params.update({'pos_hint': {'x' : 0.55, 'y': -0.2}})
        label_params.update({'text': str(AssetDict_Stats['AveragePrice']) + Currency})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Total value lbl
        label_params.update({'pos_hint': {'x' : 0.65, 'y': 0.2}})
        label_params.update({'text': 'TOTAL VALUE'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Avarage Price Value
        label_params.update({'pos_hint': {'x' : 0.65, 'y': -0.2}})
        label_params.update({'text': str(AssetDict_Stats['TotalValue']) + Currency})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Total value lbl
        label_params.update({'pos_hint': {'x' : 0.75, 'y': 0.2}})
        label_params.update({'text': 'TOTAL PROFIT'})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # Add Portfolio Asset
        color = [0,1,0,1] if AssetDict_Stats['TotalProfit'] >= 0 else [1,0,0,1]
        label_params.update({'pos_hint': {'x' : 0.75, 'y': -0.2}})
        label_params.update({'text': str(AssetDict_Stats['TotalProfit']) + Currency})
        label_params.update({'font_size': 25})
        label_params.update({'color': color})
        GraphicToReturn.add_widget(cst_item.AssetLabel(lbl_parm = label_params))

        # # Define remove button
        Btn_size = [GraphicToReturn.size[0]/2.5, GraphicToReturn.size[1]/2.5]
        box_pos_hint = {'x' : 0.9, 'y': 0.5 - (Btn_size[1]/(2*GraphicToReturn.size[1])) }

        ModifyPopup = AddAssetPopup.AddAssetPopup(title_str = 'MODIFY ASSET', type = 'M', Database = self.DBManager, PortfolioName = self.PortfolioName, itemToMod = {AssetName : AssetDict_Stats})
        RemovePopup = RemoveAssetPopup.RemoveAssetPopup('REMOVE PORTFOLIO',self.PortfolioName, AssetName, self.DBManager, self, self.FromScreenName )

        Box = cst_item.ModifyRemoveButtonBox(Btn_size = Btn_size, box_pos_hint = box_pos_hint, ModifyPopup = ModifyPopup, RemovePopup = RemovePopup)
        GraphicToReturn.add_widget(Box)

        # Return relative layout
        return GraphicToReturn

    # When the Add New Asset button is pressed
    def AddNewAssetPopup(self):
        print('Add new asset Popup')
        # Initialize the popup
        AddAssetPop = AddAssetPopup.AddAssetPopup(title_str = 'ADD NEW ASSET', type = 'A', Database = self.DBManager, PortfolioName = self.PortfolioName)
        # Open the Popup
        AddAssetPop.open()