from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.CustomItem.HoverClass import *
from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/CustomBorderButton.kv')

class CustomBorderButton(BoxLayout, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
    canvas_background_color = ColorProperty([0.1, 0.1, 0.1, 1])
    canvas_background_color_border = ColorProperty([0.1,0.1,0.5,1])
    button_size_hint = [0.5,0.5]
    button_size = [10, 10]
    border_size = ["0dp", "0dp","0dp", "0dp"]
    text = 'Select Element'
    radius = [(0,0), (0,0), (0,0), (0,0)]
    
    def __init__(self, **kwargs):
        if 'button_size_hint' in kwargs.keys():
            self.button_size_hint = kwargs['button_size_hint']
        
        if 'button_size' in kwargs.keys():
            self.button_size = kwargs['button_size']
        
        if 'border_size' in kwargs.keys():
            self.border_size = kwargs['border_size']

        if 'text' in kwargs.keys():
            self.text = kwargs['text']
        
        if 'radius' in kwargs.keys():
            self.radius = kwargs['radius']

        super().__init__()
    
    def set_color(self, mouse_in_color, mouse_out_color):
        self.BackgroundColor_mouse_out = mouse_out_color
        self.BackgroundColor_mouse_in = mouse_in_color

    def on_enter(self, *args):
        self.canvas_background_color = [0.1, 0.1, 0.2, 1]
        self.canvas_background_color_border = [0.1,0.1,0.3,0.0]
    
    def on_leave(self, *args):
        self.canvas_background_color = [0.1, 0.1, 0.1, 1]
        self.canvas_background_color_border = [0.1,0.1,0.6,0.0]