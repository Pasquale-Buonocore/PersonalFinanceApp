from Packages.CustomItem.CustomBorderButton import CustomBorderButton
from Packages.CustomItem.CustomGraphicItem import LineBoxLayout
from kivy.uix.dropdown import DropDown

class CustomDropDown():
    def __init__(self, dropdown_max_height = "150dp", ListOfButtons = [], ExternalButtonProperties = {'text': 'Select Element'}, InternalButtonProperties = {}):
        """
        ListOfButtos: it is a list of str containing all the selectionable value in the drop down 
        ExternalButtonProperties - InternalButtonProperties: they are list of properties that are used the defined the buttons in the dropdown.

        *** Excepted properties ***
        canvas_background_color: primary color used for the button. dafault: [0.5, 0.5, 0.5, 1]
        canvas_background_color_on_enter: primary color used for the button when the mouse is in. dafault: [0.5, 0.5, 0.5, 1]
        canvas_background_color_border: color used for the canvas used to visualize the border. dafault: [0.1,0.1,0.5,1]
        canvas_background_color_border_on_enter: color used for the canvas used to visualize the border when the mouse is in. dafault: [0.1,0.1,0.5,1]
        button_size_hint: size_hint property of the button. default: [None, None]
        button_size: size property of the button. default: ["10dp", "10dp"]
        border_size: if ["0dp", "0dp","0dp", "0dp"] no border is shown. It is otherwise. default: ["0dp", "0dp","0dp", "0dp"]
        text: text of the button. default: 'Button'
        radius: If ["0dp", "0dp","0dp", "0dp"] the button is not rounded. It is otherwise. default: ["0dp", "0dp","0dp", "0dp"]
        font_name: font name of the text displayed over the button. default: Arial
        font_size: font size of the text displayed over the button default: 15
        pos_hint: {'x': value_x, 'y': value_y}

        """

        self.ExternalButtonProperties = ExternalButtonProperties
        self.InternalButtonProperties = InternalButtonProperties
        self.dropdown_max_height = dropdown_max_height
        self.ListOfButtons = ListOfButtons

    def ReturnDropDownButton(self):

        # create a dropdown with 10 buttons
        dropdown = DropDown(max_height = self.dropdown_max_height)

        for ButtonName in self.ListOfButtons:
            
            # Adding internal button in drop down list
            self.InternalButtonProperties['text'] = ButtonName
            btn = CustomBorderButton(self.InternalButtonProperties)
        
            # binding the button to show the text when selected
            btn.ids['ButtonToPress'].bind(on_release = lambda btn: dropdown.select(btn.text))
        
            # then add the button inside the dropdown
            dropdown.add_widget(btn)
            # dropdown.add_widget(LineBoxLayout())

        # create a big main button
        mainbutton = CustomBorderButton(self.ExternalButtonProperties)
        mainbutton.ids['ButtonToPress'].bind(on_release = dropdown.open)

        # bind dropdown to the main button
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton.ids['ButtonToPress'], 'text', x))
        # dropdown.bind(on_dismiss = print('ciao'))

        return mainbutton