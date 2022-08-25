from Packages.DatabaseMng.AccountsManager import AccountsManager_Class
from Packages.DatabaseMng.PathManager import PathManager_Class
from Packages.DatabaseMng.JsonManager import JsonManager_Class
from Packages.CustomItem.CustomDropDown import CustomDropDown
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/SelectAccountPopup.kv')

class SelectAccountPopup(ModalView):

    def __init__(self, title_str = '', SelectedAccount = {}):
        self.Configuration = JsonManager_Class(PathManager_Class.database_path, PathManager_Class.Configuration_path)
        self.DBManager = AccountsManager_Class(PathManager_Class.database_path, PathManager_Class.Accounts_path)
        self.AvailableAccounts = list(self.DBManager.ReadJson().keys())
        self.AvailableSubAccounts = list(self.DBManager.ReadJson()[self.AvailableAccounts[0]]["SubAccount"].keys())
        self.title = title_str
        if SelectedAccount: self.SelectedAccount = SelectedAccount

        super().__init__(size_hint = (0.2,0.4))

        # Initialize popup
        self.InitializePopup()
    
    def Cancel(self):
        # Close popup at the end
        self.dismiss()
    
    # When pressing ok, the popup will save in the object that call it, the selected account (if verify is ok)
    def ConfirmAccount(self):

        # Verify if all field are correctly selected
        self.VerifySelection()

        # Close popup at the end
        self.dismiss()
    
    def VerifySelection(self):
        pass
    
    def InitializePopup(self):

        # Populate the DropDown PayingWith Account selection 
        self.ids['SelectAccountBoxLayout'].add_widget(self.DefineGeneralDropDown(self.AvailableAccounts))

        # Populate the DropDown PayingWith SubAccount selection 
        self.ids['SelectSubAccountBoxLayout'].add_widget(self.DefineGeneralDropDown(self.AvailableSubAccounts))

        # Populate Currency only if the sub account is not Asset
        self.populate_currency()

    # Initialize and return the account selection according to the account saved in DB
    def DefineGeneralDropDown(self, AvailableAccount):
        # Define external button properties
        ExternalButtonProperties = {'text' : AvailableAccount[0]}
        ExternalButtonProperties.update({'button_size_hint': [1, 1]})
        ExternalButtonProperties.update({'canvas_background_color' : self.Configuration.GetElementValue('DateFeeNoteBtnNotSelectedBackgroundColor')})
        ExternalButtonProperties.update({'canvas_background_color_on_enter' : self.Configuration.GetElementValue('DateFeeNoteBtnSelectedBackgroundColor')})
        ExternalButtonProperties.update({'radius' : [(10,10), (10,10), (10,10), (10,10)]})
        ExternalButtonProperties.update({'button_size_hint' : [0.6, 0.7]})
        ExternalButtonProperties.update({'pos_hint' : {'y' : 0.15}})
        ExternalButtonProperties.update({'font_name' : self.Configuration.GetElementValue('PopupTitleFontName')})
        ExternalButtonProperties.update({'font_size' : "17dp"})

        # Define internal button properties
        InternalButtonProperties = {}
        InternalButtonProperties.update({'button_size_hint': [1, None]})
        InternalButtonProperties.update({'button_size' : [1, 40]})
        InternalButtonProperties.update({'canvas_background_color': self.Configuration.GetElementValue('DateFeeNoteBtnNotSelectedBackgroundColor')})
        InternalButtonProperties.update({'canvas_background_color_on_enter' : self.Configuration.GetElementValue('DateFeeNoteBtnSelectedBackgroundColor')})
        InternalButtonProperties.update({'font_name' : self.Configuration.GetElementValue('PopupTitleFontName')})
        InternalButtonProperties.update({'font_size' : "17dp"})

        return CustomDropDown(ListOfButtons = AvailableAccount, ExternalButtonProperties = ExternalButtonProperties, InternalButtonProperties = InternalButtonProperties).ReturnDropDownButton()

    def populate_currency(self):
        self.ids['SelectCurrencyBoxLayout'].opacity = 0

        if self.ids['SelectSubAccountBoxLayout'].children[0].text == 'Asset': return

        # Retrieve Currenct Account and SubAccount
        Account = self.ids['SelectAccountBoxLayout'].children[0].text
        SubAccount = self.ids['SelectSubAccountBoxLayout'].children[0].text
        Currency = list(self.DBManager.ReadJson()[Account]['SubAccount'][SubAccount].keys())

        if not Currency:
            self.ids['SelectCurrencyBoxLayout'].add_widget(self.DefineGeneralDropDown(['Not available currencies\n Add them and return']))
            return
        
        self.ids['SelectCurrencyBoxLayout'].add_widget(self.DefineGeneralDropDown(Currency))
        self.ids['SelectCurrencyBoxLayout'].opacity = 1
        
