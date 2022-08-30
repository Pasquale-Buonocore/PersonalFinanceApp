from Packages.CustomFunction.HoverClass import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ColorProperty

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/PortfolioListManagement.kv')

class PortfolioLineSeparator(BoxLayout):
    pass

# class to use for each row of the portfolio list
class PortfolioRowBoxLayout(RelativeLayout, HoverBehavior):
    Background_color = ColorProperty([1,0,0,1])

    def __init__(self,**kwargs):
        # Initialize internal data
        # self.PortfolioName = kwargs['kwargs']['PortfolioName'] if ['PortfolioName'] in kwargs['kwargs'].keys() else ''
        # self.PortfolioValue = kwargs['kwargs']['Category']
        # self.NumberOfAsset = str(kwargs['kwargs']['LastMonthValue']) + str(kwargs['kwargs']['Currency'])
        # self.TotalProfit = str(kwargs['kwargs']['ValueDifference']) + str(kwargs['kwargs']['Currency'])
        # self.ToCountInAllocation = kwargs['kwargs']['ToCountInAllocation']
        # self.RowHeight = kwargs['kwargs']['RowHeight']
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('CanvasBackgroundColor')
        self.PortfolioName = 'Portfolio Name'
        self.PortfolioValue = 'Portfolio Value'
        self.NumberOfAsset = 'Number Of Asset'
        self.TotalProfit = 'Total Profit'
        self.ToCountInAllocation = 'To Count In Allocation'

        super().__init__()
    
    def on_enter(self):
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('PortfolioRowBackgroundColor_on_enter')

    def on_leave(self):
        self.Background_color = MDApp.get_running_app().Configuration.GetElementValue('CanvasBackgroundColor')


# class to use for each row of the portfolio list title
class PortfolioRowBoxLayout_Title(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__()