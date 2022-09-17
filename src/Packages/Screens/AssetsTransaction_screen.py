from Packages.CustomFunction.CustomFunction import ReturnJsonPathGivenScreenName
from Packages.CustomFunction.DefineJsonDatapath import return_updated_data_path
from Packages.DatabaseMng.PathManager import PathManager_Class
import Packages.CustomItem.Popup.AddAssetTransactionPopup as AddAssetTransactionPopup
import Packages.CustomItem.Popup.RemoveTransactionPopup as RemoveTransactionPopup
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.DatabaseMng.PortfolioManager as db_manager
from Packages.CustomItem.Lists.AssetTransactionListManagement import *
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen

class AssetsTransactionScreen(Screen):
    
    def __init__(self, **kwargs):
        # Call superclass
        super().__init__(**kwargs)
        # Graphic element which will be updated time by time
        self.ScreenToUpdate = 'AssetsTransactionHeader'

    #########################
    #    UPDATE FUNCTION    #
    #########################

    # Initialize at the asset push
    def UpdateScreen(self, AssetName, PortfolioName, PortfolioCurrency, FromScreenName):
        self.PortfolioJsonPath = ReturnJsonPathGivenScreenName(FromScreenName)
        self.FromScreenName = FromScreenName
        self.PortfolioName = PortfolioName
        self.AssetName = AssetName
        self.Currency = PortfolioCurrency
        self.DBManager = db_manager.PortfoliosManager_Class(return_updated_data_path(PathManager_Class.database_path), self.PortfolioJsonPath)

        # Update String
        self.ids['DashboardTitle'].text = self.AssetName.upper() + ' TRANSACTION HISTORY IN ' + self.PortfolioName.upper() + ' [' + self.FromScreenName.upper() + ']'

        # Update Screen
        self.UpdateListOfTransaction()

        # Update Dashboard
        # self.UpdateDashboard()

    def ReturnBack(self):
        # Return to Asset screen
        print('Returnig back to ' + self.PortfolioName + 'assets')
        ScreenManager = self.parent
        ScreenManager.current = 'ASSETS'
        # Update Asset Transaction screen
        ScreenManager.current_screen.UpdateScreen(FromScreenName = self.FromScreenName, PortfolioName = self.PortfolioName, PortfolioCurrency = self.Currency)

    ##########################
    #    TRANSACTION  BOX    #
    ##########################
    
    # Update list of transaction
    def UpdateListOfTransaction(self):
        # Clear the Item inside the BoxLayout (Keep the first element only)
        self.ids[self.ScreenToUpdate].clear_widgets()

        self.ids[self.ScreenToUpdate].add_widget(AssetTransactionLineSeparator())
        self.ids[self.ScreenToUpdate].add_widget(AssetTransactionRowBoxLayout_Title())
    

        # Then, known the PortfolioName, AssetName and having the DB, let's get all transactions
        Transactions_json = self.DBManager.ReadJson()[self.PortfolioName]['Assets'][self.AssetName]['Transactions']
        Currency_str = self.DBManager.ReadJson()[self.PortfolioName]['Statistics']['Currency']

        if len(Transactions_json.keys()):
            # Add an item for each portfolio
            for TransactionKey in list(Transactions_json.keys())[::-1]:
                self.ids[self.ScreenToUpdate].add_widget(AssetTransactionLineSeparator())

                # Compute the graphic element to Add given the PortfolioName and its statistics
                RelLayout = RelativeLayout()
                RelLayout.size_hint = [1, None]
                RelLayout.height = MDApp.get_running_app().Configuration_DB.GetElementValue('AssetRowBoxLayoutHeight')
                RelLayout.add_widget(AssetTransactionRowButton())
                AssetTransactionProperties = Transactions_json[TransactionKey]
                AssetTransactionProperties.update({'TransactionNumber': str(TransactionKey)})
                AssetTransactionProperties.update({'Currency' : Currency_str})

                # AssetProperties.update({'AssetName' : asset})
                # AssetProperties.update
                RelLayout.add_widget(AssetTransactionRowBoxLayout(Properties = AssetTransactionProperties))
                self.ids[self.ScreenToUpdate].add_widget((RelLayout))
            
            self.ids[self.ScreenToUpdate].add_widget(AssetTransactionLineSeparator())
        else:
            # Add empty item
            self.ids[self.ScreenToUpdate].add_widget(AssetTransactionRowBoxLayout_Empty())

    # Update the dashboard
    def UpdateDashboard(self):
        Json = self.DBManager.ReadJson()

        # Update asset name
        self.ids.BalanceLabel.text = self.AssetName + '(' + Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['Symbol'] + ') balance' 
   
        # Update total value
        self.ids.TotalValue.text = str(Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['TotalValue']) + Json[self.PortfolioName]['Statistics']['Currency']

        # Update Quantity
        self.ids.QuantityValue.text = str(Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['Quantity'])

        # Update Avarage Price
        self.ids.AvarageBuyValue.text = str(Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['AveragePrice']) + Json[self.PortfolioName]['Statistics']['Currency']

        # Update Total Profit
        Percentage = Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['TotalProfit'] / ((Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['AveragePrice'] * Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['Quantity']) + 1) * 100
        color = [1,0,0,1] if Percentage < 0 else [0,1,0,1]
        self.ids.TotalProfitValue.color = color
        self.ids.TotalProfitValue.text = str(Json[self.PortfolioName]['Assets'][self.AssetName]['Statistics']['TotalProfit']) + Json[self.PortfolioName]['Statistics']['Currency'] + ' (' + str(round(Percentage,1)) + '%)'
        
    # Define and empty transaction with "EMPTY" Label
    def DefineEmptyTransaction(self, textsize):
        # Get the necessary information from the AssetDictionary
        GraphicToReturn = RelativeLayout()
        GraphicToReturn.size_hint = [1, None]
        GraphicToReturn.height = "70dp"

        # Add the button with its canvas at base
        GraphicToReturn.add_widget(cst_item.EmptyTransactionButton(size_x = textsize))

        # Add AssetName label - First initialize the dict
        label_params = {}
        label_params.update({'text_size': [textsize, None]})
        label_params.update({'pos_hint': {'x' : 0.5, 'y': 0}})
        label_params.update({'text': 'EMPTY'})
        label_params.update({'font_name': 'Candarab'})
        label_params.update({'font_size': 20})
        label_params.update({'color': [1,1,1,1]})
        GraphicToReturn.add_widget(cst_item.PortfolioLabel(lbl_parm = label_params))

        # Return relative layout
        return GraphicToReturn

    # Define the transaction in input at the Box Layout
    def DefineFullTransaction(self, textsize, TransactionDict, Index, Currency):
        self.TransactionDictIndex = Index

         # Get the necessary information from the AssetDictionary
        GraphicToReturn = RelativeLayout()
        GraphicToReturn.size_hint = [1, None]
        GraphicToReturn.height = "80dp"


        # Add the button with its canvas at base
        GraphicToReturn.add_widget(cst_item.TransactionButton(size_x = textsize, height = GraphicToReturn.height))

        # Add Type Value
        label_params = {}
        label_params.update({'text_size': [textsize, None]})
        label_params.update({'pos_hint': {'x' : 0.05, 'y': 0.2}})
        label_params.update({'text': 'BUY' })
        label_params.update({'font_name': 'Candarab'})
        label_params.update({'font_size': 25})
        label_params.update({'color': [1,1,1,1]})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Date str
        label_params.update({'pos_hint': {'x' : 0.05, 'y': -0.2}})
        label_params.update({'text': TransactionDict['Date']})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Price Lbl
        label_params.update({'pos_hint': {'x' : 0.25, 'y': 0}})
        label_params.update({'text': TransactionDict['PricePerCoin'] + Currency})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Amount Value
        label_params.update({'pos_hint': {'x' : 0.4, 'y': 0}})
        label_params.update({'text': TransactionDict['Amount'] })
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Fees Lbl
        label_params.update({'pos_hint': {'x' : 0.55, 'y': 0}})
        label_params.update({'text': str(TransactionDict['Fees'])})
        label_params.update({'font_size': 20})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # Add Notes Value
        label_params.update({'pos_hint': {'x' : 0.6, 'y': 0}})
        label_params.update({'text': TransactionDict['Note']})
        label_params.update({'font_size': 25})
        GraphicToReturn.add_widget(cst_item.TransactionLabel(lbl_parm = label_params))

        # # Define remove button
        Btn_size = [GraphicToReturn.size[0]/2.5, GraphicToReturn.size[1]/2.5]
        box_pos_hint = {'x' : 0.9, 'y': 0.5 - (Btn_size[1]/(2*GraphicToReturn.size[1])) }

        ModifyPopup = AddAssetTransactionPopup.AddAssetTransactionPopup(title_str = 'MODIFY TRANSACTION', type = 'M', AssetName = self.AssetName, PortfolioName = self.PortfolioName, Database = self.DBManager, ItemToMod = {self.TransactionDictIndex: TransactionDict})
        RemovePopup = RemoveTransactionPopup.RemoveTransactionPopup(title_str = 'REMOVE TRANSACTION', PortfolioName = self.PortfolioName, AssetName = self.AssetName, TransactionIndex = Index, DBManager = self.DBManager, Screen = self, FromScreenName = self.FromScreenName )

        Box = cst_item.ModifyRemoveButtonBox(Btn_size = Btn_size, box_pos_hint = box_pos_hint, ModifyPopup = ModifyPopup, RemovePopup = RemovePopup)
        GraphicToReturn.add_widget(Box)

        # Return relative layout
        return GraphicToReturn

    # Open the Popup to add a new transaction in the DB
    def AddNewAssetTransactionPopup(self):
        print('Add new transaction to the asset Popup')
        # Initialize the popup
        AddAssetPop = AddAssetTransactionPopup.AddAssetTransactionPopup(title_str = 'ADD NEW TRANSACTION', type = 'A', AssetName = self.AssetName, PortfolioName =  self.PortfolioName, Database = self.DBManager, Currency = self.Currency)
        # Open the Popup
        AddAssetPop.open()