from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AccountsListManagement.kv')

# class to use for each row of the account list
class AccountRowBoxLayout(BoxLayout):

    def __init__(self,**kwargs):
        # Initialize internal data
        self.AccountName = kwargs['kwargs']['AccountName']
        self.Category = kwargs['kwargs']['Category']
        self.LastMonthValue = str(kwargs['kwargs']['LastMonthValue']) + str(kwargs['kwargs']['Currency'])
        self.ActualMonthValue = str(kwargs['kwargs']['ActualMonthValue']) + str(kwargs['kwargs']['Currency'])
        self.DifferenceValue = str(kwargs['kwargs']['ValueDifference']) + str(kwargs['kwargs']['Currency'])
        self.ToExpand = False
        self.RowHeight = kwargs['kwargs']['RowHeight']

        super().__init__()
    
    def ExpandAccount(self):
        # Update the Expanded property
        self.ToExpand = not self.ToExpand

        # Update the BoxLayout
        print('Expanding account ' + self.AccountName)
        self.parent.parent.parent.parent.parent.UpdateExpandedAccountList()

# class to use for the name title
class AccountRowBoxLayout_Title(BoxLayout):
    def __init__(self,**kwargs):
        # Initialize internal data
        self.AccountName = kwargs['kwargs']['AccountName']
        self.Category = kwargs['kwargs']['Category']
        self.LastMonthValue = str(kwargs['kwargs']['LastMonthValue']) + str(kwargs['kwargs']['Currency'])
        self.ActualMonthValue = str(kwargs['kwargs']['ActualMonthValue']) + str(kwargs['kwargs']['Currency'])
        self.DifferenceValue = str(kwargs['kwargs']['ValueDifference']) + str(kwargs['kwargs']['Currency'])
        self.ToExpand = False
        self.RowHeight = kwargs['kwargs']['RowHeight']

        super().__init__()

# At the end of the account, this button allwos to add a new account
class AddNewAccountBoxLayout(BoxLayout):
    def __init__(self,**kwargs):
        self.ToExpand = False
        super().__init__(**kwargs)
    
    def AddAccount(self):
        print('Adding account....')

# Box Layout containg information of the account expanded
class AccountRowExpandedBoxLayout(BoxLayout):
    def __init__(self,**kwargs):
        self.ToExpand = False
        self.RowExpansion = True
        super().__init__(**kwargs)