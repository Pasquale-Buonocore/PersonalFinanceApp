from Packages.DatabaseMng.AccountsManager import AccountsManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from kivy.uix.modalview import ModalView
from Packages.CustomFunction.HoverClass import HoverBehavior
from kivy.properties import BooleanProperty, ColorProperty
from kivy.uix.button import Button
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/SelectTransactionCategory.kv')

class CustomCategoryViewButton(Button, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
    BackgroundColor = ColorProperty(Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor'))
    SelectedStatus = BooleanProperty(False)

    def __init__(self, text = ''):
        super().__init__(size_hint =[1, None], height = "35dp", text = text)

    # on button push, the app should behave according to which button has been pressed
    def on_release(self):
        # 1. Update the Category ScrollView and the Currency ScrollView
        self.parent.parent.parent.parent.parent.SelectedCategory = self.text
        # Update button state
        self.UpdateButtonState()

    # Update the button that has been pressed
    def UpdateButtonState(self):
        # Update button background button of all buttons
        for element in self.parent.children:
            element.SelectedStatus = False
            element.BackgroundColor = self.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

        self.SelectedStatus = True
        self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 

    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

# Popup to select the transaction category
class SelectTransactionCategory(ModalView):
    ##################
    # INITIALIZATION #
    ##################
    
    def __init__(self, AvailableCategory = []):
        self.Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
        self.CategoryScrollViewBoxLayout = 'SelectCategoryScrollViewBoxLayout'
        self.AvailableCategory = AvailableCategory
        self.title = 'SELECT CATEGORY'
        self.SelectedCategory = ''
        super().__init__(size_hint = (0.2,0.4))

        # Initialize popup
        self.InitializePopup()
    
    def InitializePopup(self):
        # Populate the DropDown Account selection 
        self.SelectedCategory = self.AvailableCategory[0]

        # First clear it 
        self.ids[self.CategoryScrollViewBoxLayout].clear_widgets()
        # Then populate
        for category_name in self.AvailableCategory:
            self.ids[self.CategoryScrollViewBoxLayout].add_widget(CustomCategoryViewButton(text = category_name))
        
        if len(self.ids[self.CategoryScrollViewBoxLayout].children):
            self.ids[self.CategoryScrollViewBoxLayout].children[-1].SelectedStatus = True
            self.ids[self.CategoryScrollViewBoxLayout].children[-1].BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor')

    #####################
    # CLOSING FUNCTIONS #
    #####################
    def Cancel(self):
        # Close popup at the end
        self.dismiss()

    def ConfirmAccount(self):
        self.parent.children[1].ids['CategoryValue'].text = self.SelectedCategory
        self.parent.children[1].SelectedCategory = self.SelectedCategory

        # Close popup at the end
        self.dismiss()
