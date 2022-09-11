from Packages.CustomItem.Lists.TransactionInOutListManagement import *
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
    
    def on_enter(self):
        self.Background_color = MDApp.get_running_app().Configuration_DB.GetElementValue('AssetRowBackgroundColor_on_enter')

    def on_leave(self):
        self.Background_color = MDApp.get_running_app().Configuration_DB.GetElementValue('CanvasBackgroundColor')

# class to use for each row of the Asset list title
class TransactionInOutRowBoxLayout_Title(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__()