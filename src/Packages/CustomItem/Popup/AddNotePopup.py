from kivy.lang import Builder
from kivy.uix.modalview import ModalView

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddNotePopup.kv')

class AddNotePopup(ModalView):
    def __init__(self, note_str):
        self.note_str = note_str
        # Initialize the super class
        super().__init__(size_hint = (0.35,0.3))

    
    def Confirm(self):
        self.parent.children[1].note = self.ids['NoteValue'].text
        self.dismiss()
    
    def Cancel(self):
        self.dismiss()