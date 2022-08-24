from Packages.CustomItem.CustomBorderButton import CustomBorderButton
from Packages.CustomItem.CustomGraphicItem import LineBoxLayout
from kivy.uix.dropdown import DropDown

class CustomDropDown():
    def __init__(self, dropdown_max_height = "150dp", ListOfButtons = [], ExternalButtonProperties = {}, InternalButtonProperties = {}):
        self.dropdown_max_height = dropdown_max_height
        self.ListOfButtons = ListOfButtons

    def ReturnDropDownButton(self):

        # create a dropdown with 10 buttons
        dropdown = DropDown(max_height = self.dropdown_max_height)

        for ButtonName in self.ListOfButtons:
        
            # Adding button in drop down list
            btn = CustomBorderButton(text = ButtonName, button_size_hint = [1, None], button_size = [1, 40])
        
            # binding the button to show the text when selected
            btn.ids['ButtonToPress'].bind(on_release = lambda btn: dropdown.select(btn.text))
        
            # then add the button inside the dropdown
            dropdown.add_widget(btn)
            dropdown.add_widget(LineBoxLayout())

        # create a big main button
        mainbutton = CustomBorderButton(button_size_hint = (1, 1), radius = [(5,5), (5,5), (5,5), (5,5)]) #, pos =(350, 300))
        mainbutton.ids['ButtonToPress'].bind(on_release = dropdown.open)

        # bind dropdown to the main button
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton.ids['ButtonToPress'], 'text', x))

        return mainbutton