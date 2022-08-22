from kivy.lang import Builder
from kivy.uix.modalview import ModalView

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddFeePopup.kv')

class AddFeePopup(ModalView):
    def __init__(self, fee_str):
        self.fee_str = fee_str
        # Initialize the super class
        super().__init__(size_hint = (0.35,0.22))
    
    def Confirm(self):
        self.parent.children[1].fee = self.ids['FeeValue'].text
        self.dismiss()
    
    def Cancel(self):
        self.dismiss()