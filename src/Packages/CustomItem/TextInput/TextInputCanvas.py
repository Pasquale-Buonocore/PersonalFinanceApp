from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/TextInputCanvas.kv')

class TextInputCanvas(Widget):
    # size_hint = [0.5, 0.5]
    # text = 'Default'
    # canvas_color = [0.1, 0.1, 0.1, 1]
    # font_size = "20"

    def __init__(self, **kwargs):
        super(TextInputCanvas, self).__init__(**kwargs)

    
    # def __init__(self, size_hint = [0.2, 0.1], text = 'Default', Background_color = [0.1, 0.1, 0.1, 1], font_size = "20"):
    #     self.size_hint = size_hint
    #     self.text = text
    #     self.background_color = Background_color
    #     self.font_size = font_size
    #     super().__init__()