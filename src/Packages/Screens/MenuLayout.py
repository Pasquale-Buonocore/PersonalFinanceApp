from kivy.uix.stacklayout import StackLayout

class MenuLayout(StackLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.month = 1
        self.year = 1

    def Btn_Month(self, sign):
        pass

    def Btn_Year(self, sign):
        pass

    def UpdateAppToSelectedMonthYear(self):
        pass