from Packages.CustomItem.HoverClass import *
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle

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

    def move_screen(self, App, string):
        string = string.strip()
        print('Moving to ' + string)
        # Update current screen name
        App.root.children[0].children[0].current = string
        # Update current screen
        App.root.children[0].children[0].current_screen.UpdateScreen()

        # Update button background button of all buttons
        for element in App.root.children[0].children[1].children:
            element.SelectedStatus = False
            element.background_color = [0,0,0,0]

        self.SelectedStatus = True
        self.background_color = [0.2,0.2,1,1]
    
    def on_enter(self, *args):
        self.background_color = [0.2,0.2,1,1]
        
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.background_color = [0,0,0,0]

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
        with self.canvas.before:
            Color(0.1,0.1,0.1,0.7)
            self.shape = RoundedRectangle(size = canvas_size, radius = [(10, 10), (10, 10), (10, 10), (10, 10)])

    # At button release
    def on_release(self):
        print('Pressing Button')
    
    def on_enter(self, *args):
        self.canvas.before.children[0].rgba = [0.1,0.1,0.3,1]
        
    def on_leave(self, *args):
        self.canvas.before.children[0].rgba = [0.1,0.1,0.1,0.7]

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



