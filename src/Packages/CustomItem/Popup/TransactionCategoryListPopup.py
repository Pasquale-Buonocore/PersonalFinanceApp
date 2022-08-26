import Packages.CustomItem.Popup.AddTransactionClassPopup as AddClass_popup
import Packages.CustomItem.Popup.RemoveClassPopup as rm_class
import Packages.CustomItem.CustomGraphicItem as cst_item
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
import re

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/TransactionCategoryListPopup.kv')

class TransactionCategoryListPopup(Popup):
    def __init__(self, transaction_type = 'IN', DBManager = ''):
        super().__init__(title = 'TRANSACTION ' + transaction_type + ' CLASSES', size_hint = (0.3,0.7))

        # Define inner attributes
        self.type = transaction_type if transaction_type in ['IN','OUT'] else 'IN'
        self.DBManager = DBManager

        # Save item to modify
        self.PopulateListOfClasses()

    def PopulateListOfClasses(self):
        # Clear the ClassesTables
        self.ids['ClassesTableElements'].clear_widgets()

        # Modify text input if itemToMod is not empty
        DesiredAllocation = self.DBManager.ReadJson()[self.type]['Statistics']['DesiredAssetAllocation']
        ActualAllocation = self.DBManager.ReadJson()[self.type]['Statistics']['ActualAssetAllocation']

        for asset in DesiredAllocation.keys():
            # 1. AssetName, 2. DesiredAllocation
            Box = BoxLayout(orientation = 'horizontal', size_hint = [1, None], height = "30dp")

            # Asset Label
            AssetLabel = Label(size_hint = [0.4, None], text = asset)
            AssetLabel.text_size = [AssetLabel.width, None]
            AssetLabel.size = AssetLabel.texture_size 
            AssetLabel.height = "20dp"
            AssetLabel.font_name = 'Candarab'
            AssetLabel.font_size = 20
            AssetLabel.halign = 'center'

            # Asset desired allocation Label
            DesiredAllocationLabel = TextInput(size_hint = [0.3, None], text = str(DesiredAllocation[asset]) + '€')
            DesiredAllocationLabel.height = DesiredAllocationLabel.minimum_height
            DesiredAllocationLabel.width= DesiredAllocationLabel.height
            DesiredAllocationLabel.font_name = 'Candarab'
            DesiredAllocationLabel.font_size = 20
            DesiredAllocationLabel.halign = 'center'
            DesiredAllocationLabel.multiline = 0
            DesiredAllocationLabel.background_color = [0.5,0.5,0.5,0.7]
            DesiredAllocationLabel.foreground_color = [1,1,1,1]
            DesiredAllocationLabel.cursor_color = [1,1,1,1]

            # Define Remove button
            ThirdBoxLayout = BoxLayout(size_hint = [0.3, None], height = "20dp", orientation = 'horizontal')
            LeftBoxLayout = BoxLayout(size_hint = [0.3, None], height = "30dp")
            RightBoxLayout = BoxLayout(size_hint = [0.3, None],  height = "30dp")
            RemoveClassPopup = rm_class.RemoveClassPopup(portfolio = self.type, asset = asset, DBManager = self.DBManager, )
            RemoveBtn = cst_item.RemoveButton(Popup = RemoveClassPopup , text = 'R', size_hint = [0.4, None])
            RemoveBtn.background_color = [1,0,0,1]
            RemoveBtn.height = "30dp"

            ThirdBoxLayout.add_widget(LeftBoxLayout)
            ThirdBoxLayout.add_widget(RemoveBtn)
            ThirdBoxLayout.add_widget(RightBoxLayout)

            # Assemble
            Box.add_widget(AssetLabel)
            Box.add_widget(DesiredAllocationLabel)
            Box.add_widget(ThirdBoxLayout)

            self.ids['ClassesTableElements'].add_widget(Box)
    
    # Function to call after the "Add New push button"
    def AddNewClass(self):
        # This function opens another popup which allows to open another Popup
        Popup = AddClass_popup.AddTransactionClassPopup(self.type)
        Popup.open()

    # Function to call after the "Confirm push button"
    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        NewDesiredAllocation = {}

        # Iterate on the table elements
        for row in self.ids['ClassesTableElements'].children:
            # Extract the Asset name and value to store
            asset = row.children[2].text
            value = int(re.sub('\D', '', row.children[1].text))

            # Then modify the Desired allocation
            NewDesiredAllocation.update({asset: value})
        
        # Call the database method to modify the Desired Allocation
        self.DBManager.UpdatePortfolioDesiredAssetAllocation(PortfolioName = self.type, DictDesiredAllocation = NewDesiredAllocation)

        App.root.children[0].children[0].children[0].UpdateScreen()

        # Close the popup
        self.dismiss()

    # Function to call after the "Cencel push button"
    def Cancel(self):
        # Close the popup
        self.dismiss()