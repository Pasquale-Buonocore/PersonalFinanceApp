from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from kivy.core.window import Window
from kivy.lang import Builder
from Packages.CustomItem.TextInput.TextInputCanvas import TextInputCanvas
import datetime as dt

# Designate Out .kv design file
Builder.load_file('GraphicElement_test.kv')

class Widgets(BoxLayout):
    def __init__(self, **kwargs): 
        super(Widgets, self).__init__(**kwargs)

class P(FloatLayout):
    pass

class MyApp(MDApp):
    def build(self):
        Window.maximize()
        # Define the App configuration Database
        self.Configuration = JsonManager_Class(PathManager_Class.database_configuration_path, PathManager_Class.Configuration_path)

        return Widgets()
        
        # return TextInputCanvas( size_hint = [0.2, 0.1],
        #                        text = 'Ciao', 
        #                        Background_color = self.Configuration.GetElementValue("WindowBackgroundColor"), 
        #                        font_size = self.Configuration.GetElementValue("PopupTitleFontSize"))


if __name__ == "__main__":
    MyApp().run()