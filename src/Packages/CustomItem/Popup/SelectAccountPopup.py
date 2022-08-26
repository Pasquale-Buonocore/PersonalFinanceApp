from Packages.DatabaseMng.AccountsManager import AccountsManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from kivy.uix.modalview import ModalView
from Packages.CustomFunction.HoverClass import HoverBehavior
from kivy.properties import BooleanProperty, ColorProperty
from kivy.uix.button import Button
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/SelectAccountPopup.kv')

class CustomScrollViewButton(Button, HoverBehavior):
    Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
    BackgroundColor = ColorProperty(Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor'))
    SelectedStatus = BooleanProperty(False)

    def __init__(self, text = '', ScrollViewBoxLayoutID = ''):
        self.ScrollViewBoxLayoutID = ScrollViewBoxLayoutID
        super().__init__(size_hint =[1, None], height = "35dp", text = text)

    # on button push, the app should behave according to which button has been pressed
    def on_release(self):
        # Change current screen
        if self.ScrollViewBoxLayoutID == 'SelectAccountScrollViewBoxLayout':
            # If Account:
            # 1. Update the SubAccount ScrollView and the Currency ScrollView
            # 2. Update the button current state
            self.parent.parent.parent.parent.parent.parent.UpdateSubAccountScrollViewCurrencyScrollView(AccountName = self.text)
        
        if self.ScrollViewBoxLayoutID == 'SelectSubAccountScrollViewBoxLayout':
            # If SubAccount:
            # 1. Update the Currency ScrollView
            # 2. Update the button current state
            self.parent.parent.parent.parent.parent.parent.UpdateCurrencyScrollView(SubAccountName = self.text)
            
        if self.ScrollViewBoxLayoutID == 'SelectCurrencyScrollViewBoxLayout':
            # If Currency:
            # 1. Update the Currency
            # 2. Update the button current state
            self.parent.parent.parent.parent.parent.parent.UpdateSelectedCurrency(Currency = self.text)
            
        # Update button state
        self.UpdateButtonState()

    # Update the button that has been pressed
    def UpdateButtonState(self):
        # Update button background button of all buttons
        for element in self.parent.children:
            element.SelectedStatus = False
            element.BackgroundColor = self.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

        self.SelectedStatus = True
        self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 

    # Change Background color at entry
    def on_enter(self, *args):
        self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor') 
    
    # Change Background color at leaving
    def on_leave(self, *args):
        if not self.SelectedStatus:
            self.BackgroundColor = self.Configuration.GetElementValue('MenuButtonNotSelectedBackgroundColor') 

class SelectAccountPopup(ModalView):
    ##################
    # INITIALIZATION #
    ##################
    
    def __init__(self, title_str = '', CurrentAsset = 'Bitcoin', PortfolioCurrency = '$', type = 'storing'):
        self.Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
        self.DBManager = AccountsManager_Class(PathManager_Class.database_path, PathManager_Class.Accounts_path)
        self.AvailableAccounts = list(self.DBManager.ReadJson().keys())
        self.AvailableSubAccounts = list(self.DBManager.ReadJson()[self.AvailableAccounts[0]]["SubAccount"].keys())
        self.AccountScrollViewBoxLayout = 'SelectAccountScrollViewBoxLayout'
        self.SubAccountScrollViewBoxLayout = 'SelectSubAccountScrollViewBoxLayout'
        self.CurrencyScrollViewBoxLayout = 'SelectCurrencyScrollViewBoxLayout'
        self.title = title_str
        self.CurrentAsset = CurrentAsset
        self.SelectedAccount = {}
        self.PortfolioCurrency = PortfolioCurrency
        self.type = type
        super().__init__(size_hint = (0.4,0.4))

        # Initialize popup
        self.InitializePopup()
    
    def InitializePopup(self):
        # Populate the DropDown Account selection 
        self.PopulateScrollView(ScrollViewId = self.AccountScrollViewBoxLayout, ScrollViewButtonList = self.AvailableAccounts)
        self.SelectedAccount.update({'Account': self.AvailableAccounts[0]})

        # Populate the DropDown SubAccount selection and DropDown Currencies selection
        self.UpdateSubAccountScrollViewCurrencyScrollView(AccountName = self.AvailableAccounts[0])

    ##########################
    # SCROLL VIEW MANAGEMENT #
    ##########################

    def PopulateScrollView(self, ScrollViewId, ScrollViewButtonList):
        # First clear it 
        self.ids[ScrollViewId].clear_widgets()
        # Then populate
        for button_name in ScrollViewButtonList:
            self.ids[ScrollViewId].add_widget(CustomScrollViewButton(text = button_name, ScrollViewBoxLayoutID = ScrollViewId))
        
        if len(self.ids[ScrollViewId].children):
            self.ids[ScrollViewId].children[-1].SelectedStatus = True
            self.ids[ScrollViewId].children[-1].BackgroundColor = self.Configuration.GetElementValue('MenuButtonSelectedBackgroundColor')
    
    def UpdateSubAccountScrollViewCurrencyScrollView(self, AccountName):
        # Update the Selected Account
        self.SelectedAccount.update({'Account': AccountName})

        # Update the SubAccountScrollView
        self.PopulateScrollView(ScrollViewId = self.SubAccountScrollViewBoxLayout, ScrollViewButtonList = list(self.DBManager.ReadJson()[AccountName]["SubAccount"].keys()))
        
        # Update the CurrencyScrollView
        self.UpdateCurrencyScrollView(SubAccountName = list(self.DBManager.ReadJson()[AccountName]["SubAccount"].keys())[0])

    def UpdateCurrencyScrollView(self, SubAccountName):
        
        ##################################
        # Update the selected SubAccount #
        ##################################
        self.SelectedAccount.update({'SubAccount': SubAccountName})

        ##################################
        # Update the Currency ScrollView #
        ##################################
        CurrenciesFromDB = self.DBManager.ReadJson()[self.SelectedAccount['Account']]["SubAccount"][self.SelectedAccount['SubAccount']]
        ListOfCurrencies = list(CurrenciesFromDB.keys())

        if self.type == 'paying':
            # If I want to buy with currencies in Cash thus with STABLECOINS:
            if SubAccountName == 'Cash':
                # Show all the currencies that are self.PortfolioCurrency Equivalent
                for currency in list(CurrenciesFromDB.keys()):
                    if not (CurrenciesFromDB[currency]['Currency'] == self.PortfolioCurrency):
                        ListOfCurrencies.remove(currency)

            # TO IMPLEMENT: If I want to by with currencies not STABLECOINS
            if SubAccountName == 'Assets':
                ListOfCurrencies = []
                self.PopulateScrollView(ScrollViewId = self.CurrencyScrollViewBoxLayout, ScrollViewButtonList = ListOfCurrencies)

        else:
            # if storing, I would love to store everywhere the asset, according to the USER desire.
            # At least there will be the one we are buying.
            ListOfCurrencies = [self.CurrentAsset]

        # Operation for both
        self.PopulateScrollView(ScrollViewId = self.CurrencyScrollViewBoxLayout, ScrollViewButtonList = ListOfCurrencies)

        if not ListOfCurrencies:
            self.ids['update_message'].text = 'There is not available ' + self.PortfolioCurrency + ' for the selected subaccount. Please choose another one!'
            self.ids['Confirm'].disabled = True
            return

        self.SelectedAccount.update({'Currency': ListOfCurrencies[0]})
        self.ids['Confirm'].disabled = False
        self.ids['update_message'].text = 'Correct selection! Account: ' + self.SelectedAccount['Account'] + ' - Subaccount: ' + self.SelectedAccount['SubAccount'] + ' - Currency: ' + self.SelectedAccount['Currency']
        
    def UpdateSelectedCurrency(self, Currency):
        # Update the selected SubAccount
        self.SelectedAccount.update({'Currency': Currency})
        self.ids['update_message'].text = 'Correct selection! Account: ' + self.SelectedAccount['Account'] + ' - Subaccount: ' + self.SelectedAccount['SubAccount'] + ' - Currency: ' + self.SelectedAccount['Currency']
        self.ids['Confirm'].disabled = False


    #####################
    # CLOSING FUNCTIONS #
    #####################
    def Cancel(self):
        # Close popup at the end
        self.dismiss()
    
    def ConfirmAccount(self):
        # Save the SelectedAccount in the Popup
        if self.type == 'paying':
            self.parent.children[1].ids['ScreenManagerSection'].current_screen.ids['PayingAccountString'].text = self.SelectedAccount['Account'] + ' - ' + self.SelectedAccount['SubAccount'] + ' - ' +self.SelectedAccount['Currency']
            self.parent.children[1].SelectedPayingAccount = self.SelectedAccount
        elif self.type == 'storing':
            self.parent.children[1].SelectedStoringAccount = self.SelectedAccount
            self.parent.children[1].ids['ScreenManagerSection'].current_screen.ids['StoringAccountString'].text = self.SelectedAccount['Account'] + ' - ' + self.SelectedAccount['SubAccount'] + ' - ' +self.SelectedAccount['Currency']
        
        # Close popup at the end
        self.dismiss()