from Packages.CustomFunction.HoverClass import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ColorProperty

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/PortfolioListManagement.kv')

# When no portfolio is in the category selected, it will be shown!
class PortfolioRowBoxLayout_Empty(BoxLayout):
    pass

# Line separator used to populate the list
class PortfolioLineSeparator(BoxLayout):
    pass

# Button to use together with PortfolioRowBoxLayout to populate the ScrollView list
class PortfolioRowButton(Button):
    def __init__(self):
        super().__init__()
    
    def on_release(self):
        # Move screen from PORTFOLIO to ASSET
        self.parent.parent.parent.parent.parent.parent.parent.OpenAssetPortfolioScreen(PortfolioName = self.parent.children[0].ids.PortfolioName.text)

# class to use for each row of the portfolio list
class PortfolioRowBoxLayout(BoxLayout, HoverBehavior):
    Background_color = ColorProperty([0,0,0,1])

    def __init__(self, Properties = {}):
        # Initialize internal data
        
        # self.PortfolioValue = Properties['Category']
        # self.NumberOfAsset = str(Properties['LastMonthValue']) + str(Properties['Currency'])
        # self.TotalProfit = str(Properties['ValueDifference']) + str(Properties['Currency'])
        # self.ToCountInAllocation = Properties['ToCountInAllocation']
        # self.RowHeight = Properties['RowHeight']
        # Define background color
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('CanvasBackgroundColor')

        # Define portfolio Name
        self.PortfolioName = Properties['PortfolioName'] if 'PortfolioName' in list(Properties.keys()) else ''

        # Define Currency
        self.Currency = Properties['Currency'] if 'Currency' in list(Properties.keys()) else ''

        # Define PortfolioValue
        self.PortfolioValue = str(Properties['TotalValue']) if 'TotalValue' in list(Properties.keys()) else ''
        self.PortfolioValue += self.Currency

        # Define Number Of Asset
        self.NumberOfAsset = str(Properties['NumberOfAssets']) if 'NumberOfAssets' in list(Properties.keys()) else ''

        # Define total profit
        self.TotalProfit = str(Properties['TotalProfit']) if 'TotalProfit' in list(Properties.keys()) else ''
        self.TotalProfit += self.Currency

        # Define allocation
        self.ToCountInAllocation = 'YES' if ('ToCountInAllocation' in list(Properties.keys()) and Properties['ToCountInAllocation']) else 'NO'

        super().__init__()
    
    def on_enter(self):
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('PortfolioRowBackgroundColor_on_enter')

    def on_leave(self):
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('CanvasBackgroundColor')

# class to use for each row of the portfolio list title
class PortfolioRowBoxLayout_Title(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__()