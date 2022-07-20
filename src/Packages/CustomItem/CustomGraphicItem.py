from Packages.CustomItem.HoverClass import *
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from Packages.CustomFunction.CustomFunction import ReturnJsonPathGivenScreenName

#####################
# CUSTOM DEFINITION #
#####################
class CustomLabelMenu(Label):
    # Define properties
    SelectedStatus = BooleanProperty(False)

class CustomMenuButton(Button, HoverBehavior):
    # Define properties
    SelectedStatus = BooleanProperty(False)
    ImageName = StringProperty()

    # Function to call when moving among different portfolios
    def move_PortfolioScreen(self, App, ScreenName):
        # Define import input
        ScreenName = ScreenName.strip()
        PortfolioJsonPath = ReturnJsonPathGivenScreenName(ScreenName)

        print('Moving to ' + ScreenName)
        App.root.children[0].children[0].current = 'EMPTY'
        # Update current screen name
        App.root.children[0].children[0].current = 'PORTFOLIO'
        # Update current screen
        App.root.children[0].children[0].current_screen.UpdateScreen(ScreenName, PortfolioJsonPath)

        # Update button colors
        self.UpdateButtonState(App = App)

    # Function to call to move among different screen
    def move_screen(self, App, ScreenName):
        ScreenName = ScreenName.strip()
        print('Moving to ' + ScreenName)
        # Update current screen name
        App.root.children[0].children[0].current = ScreenName
        # Update current screen
        App.root.children[0].children[0].current_screen.UpdateScreen()

        # Update button colors
        self.UpdateButtonState(App = App)
        
    # Update the button that has been pressed
    def UpdateButtonState(self, App):
        # Update button background button of all buttons
        for element in App.root.children[0].children[1].ids.MenuListOfButton.children:
            element.SelectedStatus = False
            element.background_color = App.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

        self.SelectedStatus = True
        self.background_color = App.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 

    def on_enter(self, *args):
        self.background_color = [0.7, 0.7, 0.7, 0.5]
        # self.background_color = App.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 
        
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.background_color = [0, 0, 0, 0]
            # self.background_color = App.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

class ModifyButton(Button):
    def __init__(self,**kwargs):
        super().__init__(text = kwargs['text'], size_hint = kwargs['size_hint'])
        self.Popup = kwargs['Popup']

    def on_release(self):
        # Open the Popup
        self.Popup.open()

class RemoveButton(Button):
    def __init__(self,**kwargs):
        super().__init__(text = kwargs['text'], size_hint = kwargs['size_hint'])
        self.Popup = kwargs['Popup']

    def on_release(self):
        # Open the popup
        self.Popup.open()

class Line(Button):
    # Initialize function
    def __init__(self,**kwargs):
        super(Button, self).__init__(size_hint = [1, None], height = "3dp", background_color = [0,0,0,0])
        canvas_size = [kwargs['size_x'], super().height]       
        with self.canvas.before:
            Color(1,1,1,1)
            self.shape = Rectangle(size = canvas_size)

#######################################
# PORTFOLIO CUSTOM ELEMENT DEFINITION #
#######################################

class PortfolioLabel(Label):
    def __init__(self, **kwargs):
        # Call the superclass Label
        super().__init__()

        # Attention: The dict in input must have all key
        lbl_parm = kwargs['lbl_parm']
        self.text_size = lbl_parm['text_size']
        self.size = self.texture_size
        self.pos_hint = lbl_parm['pos_hint']
        self.text = lbl_parm['text']
        self.font_name = lbl_parm['font_name']
        self.font_size = lbl_parm['font_size']
        self.color = lbl_parm['color']

class PortfolioButton(Button, HoverBehavior):
    # Initialize function
    def __init__(self,**kwargs):
        super(Button, self).__init__(size_hint = [1, None], height = "120dp", background_color = [0,0,0,0])
        canvas_size = [kwargs['size_x'], super().height]       
        self.FromScreenName = kwargs['FromScreenName']  
        self.PortfolioName = kwargs['PortfolioName']
        with self.canvas.before:
            Color(0.1,0.1,0.1,0.8)
            self.shape = RoundedRectangle(size = canvas_size, radius = [(10, 10), (10, 10), (10, 10), (10, 10)])

    # At button release
    def on_release(self):
        print('My father screen is ' + self.FromScreenName)
        ScreenManager = self.parent.parent.parent.parent.parent.parent
        ScreenManager.current = 'ASSETS'
        ScreenManager.current_screen.UpdateScreen(FromScreenName = self.FromScreenName, PortfolioName = self.PortfolioName)
    
    def on_enter(self, *args):
        self.canvas.before.children[0].rgba = [0,0,0.3,0.8]
        
    def on_leave(self, *args):
        self.canvas.before.children[0].rgba = [0.1,0.1,0.1,0.8]

class EmptyPortfolioButton(Button):
    # Initialize function
    def __init__(self,**kwargs):
        super(Button, self).__init__(size_hint = [1, None], height = "120dp", background_color = [0,0,0,0])
        canvas_size = [kwargs['size_x'], super().height]    
        with self.canvas.before:
            Color(0.1,0.1,0.1,0.8)
            self.shape = RoundedRectangle(size = canvas_size, radius = [(10, 10), (10, 10), (10, 10), (10, 10)])

class EmptyTransactionButton(Button):
    # Initialize function
    def __init__(self,**kwargs):
        super(Button, self).__init__(size_hint = [1, None], height = "70dp", background_color = [0,0,0,0])
        canvas_size = [kwargs['size_x'], super().height]    
        with self.canvas.before:
            Color(0.1,0.1,0.1,0.8)
            self.shape = RoundedRectangle(size = canvas_size, radius = [(10, 10), (10, 10), (10, 10), (10, 10)])

class ModifyRemoveButtonBox(BoxLayout):
    def __init__(self, Btn_size, box_pos_hint, ModifyPopup = '', RemovePopup = ''):
        super().__init__()
        self.orientation = 'horizontal'
        self.pos_hint = box_pos_hint
        self.spacing = "5dp"

        # Define the first button M
        ButtonM = ModifyButton(Popup = ModifyPopup, text = 'M', size_hint = [None, None])
        ButtonM.background_color = [0,0,1,1]
        ButtonM.width = Btn_size[0]
        ButtonM.height = Btn_size[1]
        self.add_widget(ButtonM)

        # Define the first button R
        ButtonR = RemoveButton(Popup = RemovePopup, text = 'R', size_hint = [None, None])
        ButtonR.background_color = [1,0,0,1]
        ButtonR.width = Btn_size[0]
        ButtonR.height = Btn_size[1]
        self.add_widget(ButtonR)

####################################
# ASSETS CUSTOM ELEMENT DEFINITION #
####################################
class AssetLabel(Label):
     def __init__(self, **kwargs):
        # Call the superclass Label
        super().__init__()

        # Attention: The dict in input must have all key
        lbl_parm = kwargs['lbl_parm']
        self.text_size = lbl_parm['text_size']
        self.size = self.texture_size
        self.pos_hint = lbl_parm['pos_hint']
        self.text = lbl_parm['text']
        self.font_name = lbl_parm['font_name']
        self.font_size = lbl_parm['font_size']
        self.color = lbl_parm['color']

class AssetButton(Button, HoverBehavior):
    # Initialize function
    def __init__(self,**kwargs):
        super(Button, self).__init__(size_hint = [1, None], height = "120dp", background_color = [0,0,0,0])
        canvas_size = [kwargs['size_x'], super().height]       
        self.FromScreenName = kwargs['FromScreenName']  
        self.PortfolioName = kwargs['PortfolioName']
        self.AssetName = kwargs['AssetName']

        with self.canvas.before:
            Color(0.1,0.1,0.1,0.8)
            self.shape = RoundedRectangle(size = canvas_size, radius = [(10, 10), (10, 10), (10, 10), (10, 10)])

    # At button release
    def on_release(self):
        print('Moving on transaction screen for the asset ' + self.AssetName + ' in the ' + self.PortfolioName + ' portfolio - ' + ' Screen: '+ self.FromScreenName)
        ScreenManager = self.parent.parent.parent.parent.parent.parent
        ScreenManager.current = 'ASSETS TRANSACTION'
        ScreenManager.current_screen.UpdateScreen(self.AssetName, self.PortfolioName, self.FromScreenName)
    
    def on_enter(self, *args):
        self.canvas.before.children[0].rgba = [0,0,0.3,0.8]
        
    def on_leave(self, *args):
        self.canvas.before.children[0].rgba = [0.1,0.1,0.1,0.8]

#########################################
# TRANSACTION CUSTOM ELEMENT DEFINITION #
#########################################
class TransactionLabel(Label):
     def __init__(self, **kwargs):
        # Call the superclass Label
        super().__init__()

        # Attention: The dict in input must have all key
        lbl_parm = kwargs['lbl_parm']
        self.text_size = lbl_parm['text_size']
        self.size = self.texture_size
        self.pos_hint = lbl_parm['pos_hint']
        self.text = lbl_parm['text']
        self.font_name = lbl_parm['font_name']
        self.font_size = lbl_parm['font_size']
        self.color = lbl_parm['color']

class TransactionButton(Button, HoverBehavior):
    # Initialize function
    def __init__(self,**kwargs):
        super(Button, self).__init__(size_hint = [1, None], height = kwargs['height'], background_color = [0,0,0,0])
        canvas_size = [kwargs['size_x'], super().height]       

        with self.canvas.before:
            Color(0.1,0.1,0.1,0.8)
            self.shape = RoundedRectangle(size = canvas_size, radius = [(0, 0), (0, 0), (0, 0), (0, 0)])
    
    def on_enter(self, *args):
        self.canvas.before.children[0].rgba = [0,0,0.3,0.8]
        
    def on_leave(self, *args):
        self.canvas.before.children[0].rgba = [0.1,0.1,0.1,0.8]

