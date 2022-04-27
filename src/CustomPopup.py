from kivy.lang import Builder
from kivy.uix.popup import Popup
import DatabaseMng as db_manager

# Designate Out .kv design file
Builder.load_file('ui/PopupMng.kv')

class WarningPopup(Popup):
    def __init__(self, title_str, message):
        self.MessageToDisplay = message
        super().__init__(title = title_str, size_hint=(0.25,0.3))

class RemovingPopup(Popup):
    def __init__(self, ManagerOfItem, ManagerOfScreen, DBManager, title_str = 'REMOVING WARNING'):
        super().__init__(title = title_str, size_hint=(0.25,0.2))
        self.ManagerOfItem = ManagerOfItem
        self.ManagerOfScreen = ManagerOfScreen
        self.DBManager = DBManager

    def RemoveIt(self):
        # When the remove button is pressed, the item should be removed from the json. The UI shall be updated as well.
        # Remove widget from the Json
        self.DBManager.RemoveElement(self.ManagerOfItem)
        # Update the UI
        self.ManagerOfScreen.Update_InFlowBoxLayout()
        # Close the popup
        self.dismiss()

class InFlowPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        # Define inner attributes
        self.type = type if type in ['A','M'] else'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        self.ids["Location_Input"].text = list(self.itemToMod.keys())[0]
        self.ids["LastMonth_Input"].text = str(self.itemToMod[self.ids["Location_Input"].text][0])
        self.ids["ThisMonth_Input"].text = str(self.itemToMod[self.ids["Location_Input"].text][1])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "LOCATION INPUT" from Text Input - In empty do nothing
        Location_Input = self.ids["Location_Input"].text.replace(" ", "")
        if not Location_Input: string = string + 'ERROR: Empty location FIELD\n\n'

        # Retrive data "LastMonth_Input" from Text Input - In empty do nothing
        LastMonth_Input = self.ids["LastMonth_Input"].text.replace(" ", "")
        if not LastMonth_Input: string = string + 'ERROR: Empty last month value FIELD\n\n'
        if not LastMonth_Input.replace(".", "").isnumeric(): string = string + 'ERROR: last month must be numeric FIELD\n\n'

        # Retrive data "ThisMonth_Input" from Text Input - In empty do nothing
        ThisMonth_Input = self.ids["ThisMonth_Input"].text.replace(" ", "")
        if not ThisMonth_Input: string = string + 'ERROR: Empty this month value FIELD'
        if not ThisMonth_Input.replace(".", "").isnumeric(): string =string + 'ERROR: this month must be numeric FIELD\n\n'

        if string:
            # If the error message is not empty, display an error
            Pop = WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            Dashboard_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].InFlow_DBmanager
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
        self.dismiss()