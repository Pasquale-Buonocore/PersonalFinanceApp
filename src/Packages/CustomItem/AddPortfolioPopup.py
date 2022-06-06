from kivy.lang import Builder
from kivy.uix.popup import Popup
import Packages.CustomItem.WarningPopup as Wrn_popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddPortfolioPopup.kv')

class AddPortfolioPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint = (0.3,0.5))

        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        ItemName = list(self.itemToMod.keys())[0]
        self.ids["CurrencyValue"].text = str(self.itemToMod[ItemName]['Currency'])
        self.ids["PortfolioName"].text = ItemName

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Portfolio Name" from Text Input - In empty do nothing
        PortfolioValue = self.ids["PortfolioName"].text.strip().upper()
        if not PortfolioValue: string = string + 'ERROR: Empty asset name FIELD'

        # Retrive data "Currency Value" from Text Input - In empty do nothing
        CurrencySymbol = self.ids["CurrencyValue"].text.strip().upper()
        if not CurrencySymbol: string = string + '\nERROR: Empty symbol value FIELD'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
        else:
            # Instantiate Screen and Json manager
            Dashboard_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].InFlow_DBManager
            New_Element = {Location_Input:[float(LastMonth_Input), float(ThisMonth_Input)]}
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElement(Old_element = self.itemToMod, New_Item = New_Element)
            else:
                # Append new item
                Json_mng.AddElement(New_Element)

            # Update the Json and Update the Dashboard Screen
            Dashboard_Scr.Update_InFlowBoxLayout()


            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()