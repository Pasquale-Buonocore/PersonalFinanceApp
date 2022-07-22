from kivy.uix.stacklayout import StackLayout
import datetime as dt

class MenuLayout(StackLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.current_date = dt.datetime.now()

        # Internal initial value
        self.month = self.current_date.month
        self.year = self.current_date.year

        # Update string
        self.SelectedMonth = self.current_date.strftime("%B") 
        self.SelectedYear = str(self.year)

    def GetMonthNameFromNumber(self, MonthNumber):
        return dt.datetime(1, int(MonthNumber), 1).strftime("%B") 

    def Btn_Month(self, sign):
        if sign == '-':
            self.month -= 1
            self.month = 12 if not self.month else self.month

        elif sign == '+':
            self.month += 1
            self.month = 1 if self.month > 12 else self.month
        
        self.SelectedMonth = self.GetMonthNameFromNumber(self.month)
        self.ids.MonthStringValue.text = self.SelectedMonth


    def Btn_Year(self, sign):
        if sign == '-':
            self.year-= 1
        elif sign == '+':
            self.year += 1
        
        self.SelectedYear  = str(self.year)
        self.ids.YearStringValue.text = self.SelectedYear

    def UpdateAppToSelectedMonthYear(self):
        pass