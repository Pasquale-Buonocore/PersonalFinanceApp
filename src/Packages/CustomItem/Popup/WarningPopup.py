from kivy.lang import Builder
from kivy.uix.popup import Popup

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/WarningPopup.kv')

class WarningPopup(Popup):
    def __init__(self, title_str, message):
        self.MessageToDisplay = message
        super().__init__(title = title_str, size_hint=(0.25,0.4))