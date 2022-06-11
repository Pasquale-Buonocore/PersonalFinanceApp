from Packages.CustomFunction.CustomFunction import ReturnJsonPathGivenScreenName
import Packages.CustomItem.AddAssetTransactionPopup as AddAssetTransactionPopup
import Packages.CustomItem.RemoveAssetPopup as RemoveAssetPopup
import Packages.CustomItem.CustomGraphicItem as cst_item
import Packages.DatabaseMng.DatabaseMng as db_manager
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
    def UpdateScreen(self, AssetName, PortfolioName, FromScreenName):
        self.PortfolioJsonPath = ReturnJsonPathGivenScreenName(FromScreenName)
        self.FromScreenName = FromScreenName
        self.PortfolioName = PortfolioName
        self.AssetName = AssetName
        self.DBManager = db_manager.PortfoliosManager_Class(db_manager.path_manager.database_path, self.PortfolioJsonPath)

        # Update String
        self.ids['FirstRowLabel'].text = self.AssetName.upper() + ' TRANSACTION HISTORY IN ' + self.PortfolioName.upper() + ' [' + self.FromScreenName.upper() + ']'

        # Update Screen
        self.UpdateListOfTransaction()

    def ReturnBack(self):
        # Return to Asset screen
        print('Returnig back to ' + self.PortfolioName + 'assets')
        ScreenManager = self.parent
        ScreenManager.current = 'ASSETS'
        # Update Asset Transaction screen
        ScreenManager.current_screen.UpdateScreen(FromScreenName = self.FromScreenName, PortfolioName = self.PortfolioName)

    ##########################
    #    TRANSACTION  BOX    #
    ##########################
    
    # Update list of transaction
    def UpdateListOfTransaction(self):
        # Store the first Item and second Item containing:
        First_widget = self.ids[self.ScreenToUpdate].children[-1] # contains the first row of Return to Asset, Title, Add new Transaction
        Second_widget = self.ids[self.ScreenToUpdate].children[-2] # Contains the label of title

        # Store the BoxLayout containg the portfolios Relative layout
        Third_widget = self.ids[self.ScreenToUpdate].children[-3]  
        Third_widget.clear_widgets()

        # Clear the Item inside the BoxLayout (Keep the first element only)
        self.ids[self.ScreenToUpdate].clear_widgets()

        # Add the first and second item again
        self.ids[self.ScreenToUpdate].add_widget(First_widget)
        self.ids[self.ScreenToUpdate].add_widget(Second_widget)
        self.ids[self.ScreenToUpdate].add_widget(Third_widget)

        # Then, known the PortfolioName, AssetName and having the DB, let's get all transactions
        Transactions_json = self.DBManager.ReadJson()[self.PortfolioName]['Assets'][self.AssetName]['Transactions']

        # Get the Currency of such Portfolio
        Currency_str = self.DBManager.ReadJson()[self.PortfolioName]['Statistics']['Currency']

        # Size dello ScreenManager
        ScreenManagerSize_x = self.parent.size[0]
        BoxLayoutPadding_ls= self.children[0].children[0].padding[0]
        BoxLayoutPadding_rs = self.children[0].children[0].padding[2]
        text_size = ScreenManagerSize_x - BoxLayoutPadding_ls - BoxLayoutPadding_rs

        if len(Transactions_json.keys()):
            # Add an item for each portfolio
            for TransactionKey in Transactions_json.keys():
                # Compute the graphic element to Add given the AssetName and its statistics
                self.ids[self.ScreenToUpdate].children[-3].add_widget(self.DefineFullTransaction(textsize = text_size, TransactionDict = Transactions_json[TransactionKey], Index = TransactionKey , Currency = Currency_str))
        else:
            # Add empty item
            self.ids[self.ScreenToUpdate].children[-3].add_widget(self.DefineEmptyTransaction(textsize = text_size))


    # Define and empty transaction with "EMPTY" Label
    def DefineEmptyTransaction(self, textsize):
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
        label_params.update({'text': TransactionDict['Type'] })
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
        label_params.update({'text': TransactionDict['Price'] + Currency})
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
        # RemovePopup = RemoveAssetPopup.RemoveAssetPopup('REMOVE PORTFOLIO',self.PortfolioName, AssetName, self.DBManager, self, self.FromScreenName )

        Box = cst_item.ModifyRemoveButtonBox(Btn_size = Btn_size, box_pos_hint = box_pos_hint, ModifyPopup = ModifyPopup, RemovePopup = ModifyPopup)
        GraphicToReturn.add_widget(Box)

        # Return relative layout
        return GraphicToReturn

    # Open the Popup to add a new transaction in the DB
    def AddNewAssetTransactionPopup(self):
        print('Add new transaction to the asset Popup')
        # Initialize the popup
        AddAssetPop = AddAssetTransactionPopup.AddAssetTransactionPopup(title_str = 'ADD NEW TRANSACTION', type = 'A', AssetName = self.AssetName, PortfolioName =  self.PortfolioName, Database = self.DBManager)
        # Open the Popup
        AddAssetPop.open()