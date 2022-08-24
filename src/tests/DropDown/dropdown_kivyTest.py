# Program to explain how to create drop-down in kivy
    
# import kivy module   
from kivy.app import App
from kivymd.app import MDApp
    
# Importing Drop-down from the module to use in the program
from Packages.CustomItem.CustomDropDown import CustomDropDown
from kivy.uix.relativelayout import RelativeLayout
from Packages.CustomItem.HoverClass import *

 
# another way used to run kivy app
from kivy.lang import Builder
Builder.load_file('dropdown_kivyTest.kv')

class MainLayout(RelativeLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class MyApp(MDApp):
    def build(self):
        Main = MainLayout()
        Main.pos_hint = {'x': 0.25, 'y': 0.5}
        Accounts = ['Unicredit Accounts', 'Ledger' , 'DeGiro']
        Main.add_widget(CustomDropDown(ListOfButtons = Accounts).ReturnDropDownButton())

        return Main

if __name__ == "__main__":
    MyApp().run()