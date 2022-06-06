from kivy.lang import Builder
from kivy.uix.popup import Popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/RemovingPopup.kv')

class RemovingPopup(Popup):
    def __init__(self, ManagerOfItem, ManagerOfScreen, DBManager, UpdateFunction_str, RemoveFunction = 'RemoveElement', title_str = 'REMOVING WARNING'):
        super().__init__(title = title_str, size_hint=(0.25,0.2))
        self.ManagerOfItem = ManagerOfItem
        self.ManagerOfScreen = ManagerOfScreen
        self.DBManager = DBManager
        self.UpdateFunction_str = UpdateFunction_str
        self.RemoveFunction_str = RemoveFunction

    def RemoveIt(self):
        # When the remove button is pressed, the item should be removed from the json. The UI shall be updated as well.

        # Remove widget from the Json
        getattr(self.DBManager, self.RemoveFunction_str)(self.ManagerOfItem)
        # Update the UI
        getattr(self.ManagerOfScreen, self.UpdateFunction_str)()
        # Close the popup
        self.dismiss()