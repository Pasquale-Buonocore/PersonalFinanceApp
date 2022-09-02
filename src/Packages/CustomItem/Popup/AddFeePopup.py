from Packages.CustomFunction.CustomFunction import verify_numeric_float_string
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddFeePopup.kv')

class AddFeePopup(ModalView):
    def __init__(self, fee_str):
        self.fee_str = fee_str
        # Initialize the super class
        super().__init__(size_hint = (0.35,0.22))
    
    def verify_input(self):
        # Check correctness
        if ('%s' % self.ids['FeeValue'].text).replace('.','').replace(',','').isnumeric():
            self.ids['FeeValue'].text = verify_numeric_float_string(self.ids['FeeValue'].text)
        else:
            self.ids['FeeValue'].text = '0.0'
        
    def Confirm(self):
        self.parent.children[1].fee = self.ids['FeeValue'].text
        self.dismiss()
    
    def Cancel(self):
        self.dismiss()