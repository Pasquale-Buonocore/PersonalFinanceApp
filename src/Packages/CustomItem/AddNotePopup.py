from kivy.lang import Builder
from kivy.uix.modalview import ModalView

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddNotePopup.kv')

class AddNotePopup(ModalView):
    def __init__(self, **kwargs):
        # Initialize the super class
        super().__init__(size_hint = (0.35,0.3))