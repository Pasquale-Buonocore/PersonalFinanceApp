from Packages.CustomFunction.HoverClass import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ColorProperty

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AssetListManagement.kv')

# When no Asset is in the category selected, it will be shown!
class AssetRowBoxLayout_Empty(BoxLayout):
    pass

# Line separator used to populate the list
class AssetLineSeparator(BoxLayout):
    pass

# Button to use together with AssetRowBoxLayout to populate the ScrollView list
class AssetRowButton(Button):
    def __init__(self):
        super().__init__()
    
    def on_release(self):
        # Move screen from Asset to ASSET
        self.parent.parent.parent.parent.parent.parent.parent.OpenAssetTransactionScreen(AssetName = self.parent.children[0].ids.AssetName.text)

# class to use for each row of the Asset list
class AssetRowBoxLayout(BoxLayout, HoverBehavior):
    Background_color = ColorProperty([0,0,0,1])

    def __init__(self, Properties = {}):        
        # Define background color
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('CanvasBackgroundColor')

        # Define Asset Name
        self.AssetName = Properties['AssetName'] if 'AssetName' in list(Properties.keys()) else ''
        self.AssetSymbol = Properties['Symbol'] if 'Symbol' in list(Properties.keys()) else ''

        # Define Currency
        self.Currency = Properties['Currency'] if 'Currency' in list(Properties.keys()) else ''

        # Define CurrentPrice
        self.CurrentPrice = str(Properties['CurrentPrice']) if 'CurrentPrice' in list(Properties.keys()) else ''
        self.CurrentPrice += self.Currency

        # Define Holding
        self.Holding = str(Properties['Quantity']) if 'Quantity' in list(Properties.keys()) else ''

        # Define Average Price
        self.AveragePrice = str(Properties['AveragePrice']) if 'AveragePrice' in list(Properties.keys()) else ''
        self.AveragePrice += self.Currency
        
        # Define Total Value
        self.TotalValue = str(Properties['TotalValue']) if 'TotalValue' in list(Properties.keys()) else ''
        self.TotalValue += self.Currency

        # Define total profit
        self.TotalProfit = str(Properties['TotalProfit']) if 'TotalProfit' in list(Properties.keys()) else ''
        self.TotalProfit += self.Currency

        super().__init__()
    
    def on_enter(self):
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('AssetRowBackgroundColor_on_enter')

    def on_leave(self):
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('CanvasBackgroundColor')

# class to use for each row of the Asset list title
class AssetRowBoxLayout_Title(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__()