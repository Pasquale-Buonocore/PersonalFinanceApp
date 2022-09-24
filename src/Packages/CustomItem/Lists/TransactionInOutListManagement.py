from Packages.CustomItem.Lists.TransactionInOutListManagement import *
from Packages.CustomFunction.CustomFunction import return_account_dict_given_account_element_list
from Packages.CustomFunction.HoverClass import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ColorProperty

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/TransactionInOutListManagement.kv')



# When no Asset is in the category selected, it will be shown!
class TransactionInOutRowBoxLayout_Empty(BoxLayout):
    pass

# Line separator used to populate the list
class TransactionInOutLineSeparator(BoxLayout):
    pass

# Button to use together with AssetRowBoxLayout to populate the ScrollView list
class TransactionInOutRowButton(Button):
    def __init__(self):
        super().__init__()
    
# class to use for each row of the Asset list
class TransactionInOutRowBoxLayout(BoxLayout, HoverBehavior):
    Background_color = ColorProperty([0,0,0,1])

    def __init__(self, Properties = {}):        
        # Define background color
        self.Background_color = MDApp.get_running_app().Configuration_DB.GetElementValue('CanvasBackgroundColor')

        # Transaction Number
        self.TransactionNumber = Properties['TransactionNumber'] if 'TransactionNumber' in list(Properties.keys()) else ''

        # Date
        self.Date = Properties['Date'] if 'Date' in list(Properties.keys()) else ''

        # Define Currency
        self.Currency = Properties['Currency'] if 'Currency' in list(Properties.keys()) else ''

        # Define Category
        self.Category = str(Properties['Category']) if 'Category' in list(Properties.keys()) else ''

        # Define Amount
        self.Amount = str(Properties['Amount']) if 'Amount' in list(Properties.keys()) else ''
        self.Amount += self.Currency

        # Define Paying Account
        # self.PayingAccount_Account = 'Account: ' + str(Properties['PayingAccount']['Account']) if 'PayingAccount' in list(Properties.keys()) else ''
        # self.PayingAccount_SubAccount = 'Sub: ' + str(Properties['PayingAccount']['SubAccount']) if 'PayingAccount' in list(Properties.keys()) else ''
        #self.PayingAccount_Asset = 'Asset: ' + str(Properties['PayingAccount']['Currency']) if 'PayingAccount' in list(Properties.keys()) else ''
        self.PayingAccount = str(Properties['PayingAccount']) if 'PayingAccount' in list(Properties.keys()) else '---'
        
        # Define Note
        self.Description = str(Properties['Note']) if ('Note' in list(Properties.keys()) and Properties["Note"])  else '---'

        super().__init__()
    
    def Modify_transaction(self) -> None:
        print('Modify transaction')

    def Remove_transaction(self) -> None:

        # Define connection to databases and portfolio name
        Transaction_database = self.parent.parent.parent.parent.DBManager
        Portfolio_name = self.parent.parent.parent.parent.portfolio
        Portfolio_list_name = self.parent.parent.parent.parent.portfolio_list

        # Extract info from current transaction
        Transaction_Linking_code = Transaction_database.ReadJson()[Portfolio_list_name]['Assets']['Transactions']['Transactions'][self.TransactionNumber]['LinkingCode']
        Transaction_Index = self.TransactionNumber
        Transaction_Category = self.Category
        Transaction_PayingAccount_dict = return_account_dict_given_account_element_list(self.PayingAccount)

        # First Remove transaction from the <IN_OUT>_LIST json
        Transaction_database.RemoveTransactionFromAssetList(PortfolioName = Portfolio_list_name, AssetName = 'Transactions', ItemIndex = Transaction_Index)
        
        # Then Remove Transaction from the <IN> json based on Linking Code
        Transaction_database.RemoveTransactionFromAssetListBasedOnLikingCode(PortfolioName = Portfolio_list_name, AssetName = Transaction_Category, Linking_Code = Transaction_Linking_code)
        
        # Then Remove Transaction from Account
        MDApp.get_running_app().Accounts_DB.RemoveMonthlyTransactionBasedOnLinkingCode(AccountName = Transaction_PayingAccount_dict['Account'],
                                                                                       SubAccountName = Transaction_PayingAccount_dict['SubAccount'],
                                                                                       CurrencyName = Transaction_PayingAccount_dict['Currency'], 
                                                                                       LinkingCode = Transaction_Linking_code)
        # Update Paying Account statistics
        MDApp.get_running_app().Accounts_DB.Update_liquid_investing_balance(Transaction_PayingAccount_dict['Account'], Transaction_PayingAccount_dict['SubAccount'], Transaction_PayingAccount_dict['Currency'])

        # Update Asset Statistics in transaction list
        Transaction_database.UpdateAssetInTransactionStatistics(Portfolio_name, Transaction_Category)


    def on_enter(self):
        self.Background_color = MDApp.get_running_app().Configuration_DB.GetElementValue('AssetRowBackgroundColor_on_enter')

    def on_leave(self):
        self.Background_color = MDApp.get_running_app().Configuration_DB.GetElementValue('CanvasBackgroundColor')

# class to use for each row of the Asset list title
class TransactionInOutRowBoxLayout_Title(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__()