from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from Packages.CustomItem.HoverClass import *

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