from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.CustomFunction.HoverClass import *
from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/CustomBorderButton.kv')

class CustomBorderButton(BoxLayout, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)
    canvas_background_color = ColorProperty([0.1, 0.1, 0.1,1])
    canvas_background_color_on_enter = ColorProperty([0.5, 0.5, 0.5,1])
    canvas_background_color_on_leave = ColorProperty([0.1, 0.1, 0.1,1])
    canvas_background_color_border = ColorProperty([0.1,0.1,0.5,1])
    canvas_background_color_border_on_enter = ColorProperty([0.1,0.1,0.9,1])
    canvas_background_color_border_on_leave = ColorProperty([0.1,0.1,0.5,1])
    button_size_hint = [None, None]
    button_size = ["50dp", "50dp"]
    border_size = ["0dp", "0dp","0dp", "0dp"]
    text = 'Button'
    radius = [(0,0), (0,0), (0,0), (0,0)]
    font_size = 15
    font_name = ''
    pos_hint = {'x' : 0, 'y' : 0}
    
    def __init__(self, ButtonProperty):

        if 'canvas_background_color' in ButtonProperty.keys():
            self.canvas_background_color = ButtonProperty['canvas_background_color']
            self.canvas_background_color_on_leave = ButtonProperty['canvas_background_color']
        
        if 'canvas_background_color_on_enter' in ButtonProperty.keys():
            self.canvas_background_color_on_enter = ButtonProperty['canvas_background_color_on_enter']
            
        if 'canvas_background_color_border' in ButtonProperty.keys():
            self.canvas_background_color_border = ButtonProperty['canvas_background_color_border']
            self.canvas_background_color_border_on_leave = ButtonProperty['canvas_background_color_border']
            
        if 'canvas_background_color_border_on_enter' in ButtonProperty.keys():
            self.canvas_background_color_border_on_enter = ButtonProperty['canvas_background_color_border_on_enter']
            
        if 'button_size_hint' in ButtonProperty.keys():
            self.button_size_hint = ButtonProperty['button_size_hint']
        
        if 'button_size' in ButtonProperty.keys():
            self.button_size = ButtonProperty['button_size']
        
        if 'border_size' in ButtonProperty.keys():
            self.border_size = ButtonProperty['border_size']

        if 'text' in ButtonProperty.keys():
            self.text = ButtonProperty['text']
        
        if 'radius' in ButtonProperty.keys():
            self.radius = ButtonProperty['radius']      

        if 'font_size' in ButtonProperty.keys():
            self.font_size = ButtonProperty['font_size']        
        
        if 'font_name' in ButtonProperty.keys():
            self.font_name = ButtonProperty['font_name']
        
        if 'pos_hint' in ButtonProperty.keys():
            self.pos_hint = ButtonProperty['pos_hint']

        super().__init__()
    
    def on_enter(self, *args):
        self.canvas_background_color = self.canvas_background_color_on_enter
        self.canvas_background_color_border = self.canvas_background_color_border_on_enter
    
    def on_leave(self, *args):
        self.canvas_background_color = self.canvas_background_color_on_leave
        self.canvas_background_color_border = self.canvas_background_color_on_leave