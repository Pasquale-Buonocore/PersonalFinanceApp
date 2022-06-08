import Packages.CustomItem.WarningPopup as Wrn_popup
from kivy.uix.popup import Popup
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('ui/PopupMng.kv')

###################
# ADD TRANSACTION #
###################

class InFlowPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        self.ids["Location_Input"].text = list(self.itemToMod.keys())[0]
        self.ids["LastMonth_Input"].text = str(self.itemToMod[self.ids["Location_Input"].text][0])
        self.ids["ThisMonth_Input"].text = str(self.itemToMod[self.ids["Location_Input"].text][1])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "LOCATION INPUT" from Text Input - In empty do nothing
        Location_Input = self.ids["Location_Input"].text.strip()
        if not Location_Input: string = string + 'ERROR: Empty location FIELD\n'

        # Retrive data "LastMonth_Input" from Text Input - In empty do nothing
        LastMonth_Input = self.ids["LastMonth_Input"].text.strip()
        if not LastMonth_Input: string = string + 'ERROR: Empty last month value FIELD\n'
        if not LastMonth_Input.replace(".", "").isnumeric(): string = string + 'ERROR: last month must be numeric FIELD\n'

        # Retrive data "ThisMonth_Input" from Text Input - In empty do nothing
        ThisMonth_Input = self.ids["ThisMonth_Input"].text.strip()
        if not ThisMonth_Input: string = string + 'ERROR: Empty this month value FIELD\n'
        if not ThisMonth_Input.replace(".", "").isnumeric(): string =string + 'ERROR: this month must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            Dashboard_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].InFlow_DBManager
            New_Element = {Location_Input:[float(LastMonth_Input), float(ThisMonth_Input)]}
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElement(Old_element = self.itemToMod, New_Item = New_Element)
            else:
                # Append new item
                Json_mng.AddElement(New_Element)

            # Update the Json and Update the Dashboard Screen
            Dashboard_Scr.Update_InFlowBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        self.dismiss()

class ExpencesPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        self.ids["ExpencesCategory"].text = list(self.itemToMod.keys())[0]
        self.ids["Expences_ForeseenValue"].text = str(self.itemToMod[self.ids["ExpencesCategory"].text][0])
        self.ids["Expences_ActualValue"].text = str(self.itemToMod[self.ids["ExpencesCategory"].text][1])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "ExpencesCategory" from Text Input - In empty do nothing
        ExpencesCategory = self.ids["ExpencesCategory"].text.strip()
        if not ExpencesCategory: string = string + 'ERROR: Empty category FIELD\n'

        # Retrive data "Expences_ForeseenValue" from Text Input - In empty do nothing
        Expences_ForeseenValue = self.ids["Expences_ForeseenValue"].text.strip()
        if not Expences_ForeseenValue: string = string + 'ERROR: Empty Foreseen value FIELD\n'
        if not Expences_ForeseenValue.replace(".", "").isnumeric(): string = string + 'ERROR: Foreseen value must be numeric FIELD\n'

        # Retrive data "Expences_ActualValue" from Text Input - In empty do nothing
        Expences_ActualValue = self.ids["Expences_ActualValue"].text.strip()
        if not Expences_ActualValue: string = string + 'ERROR: Empty actual value FIELD\n'
        if not Expences_ActualValue.replace(".", "").isnumeric(): string =string + 'ERROR: Actual value must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            Dashboard_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].Expences_DBManager
            New_Element = {ExpencesCategory:[float(Expences_ForeseenValue), float(Expences_ActualValue)]}
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElement(Old_element = self.itemToMod, New_Item = New_Element)
            else:
                # Append new item
                Json_mng.AddElement(New_Element)

            # Update the Json and Update the Dashboard Screen
            Dashboard_Scr.Update_ExpencesBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

class EarningsPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        self.ids["EarningsCategory"].text = list(self.itemToMod.keys())[0]
        self.ids["Earnings_ForeseenValue"].text = str(self.itemToMod[self.ids["EarningsCategory"].text][0])
        self.ids["Earnings_ActualValue"].text = str(self.itemToMod[self.ids["EarningsCategory"].text][1])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "EarningsCategory" from Text Input - In empty do nothing
        EarningsCategory = self.ids["EarningsCategory"].text.strip()
        if not EarningsCategory: string = string + 'ERROR: Empty category FIELD\n'

        # Retrive data "Earnings_ForeseenValue" from Text Input - In empty do nothing
        Earnings_ForeseenValue = self.ids["Earnings_ForeseenValue"].text.strip()
        if not Earnings_ForeseenValue: string = string + 'ERROR: Empty foressen value FIELD\n'
        if not Earnings_ForeseenValue.replace(".", "").isnumeric(): string = string + 'ERROR: Foreseen value must be numeric FIELD\n'

        # Retrive data "Earnings_ActualValue" from Text Input - In empty do nothing
        Earnings_ActualValue = self.ids["Earnings_ActualValue"].text.strip()
        if not Earnings_ActualValue: string = string + 'ERROR: Empty actual value FIELD\n'
        if not Earnings_ActualValue.replace(".", "").isnumeric(): string =string + 'ERROR: Actual value must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            Dashboard_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].Earnings_DBManager
            New_Element = {EarningsCategory:[float(Earnings_ForeseenValue), float(Earnings_ActualValue)]}
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElement(Old_element = self.itemToMod, New_Item = New_Element)
            else:
                # Append new item
                Json_mng.AddElement(New_Element)

            # Update the Json and Update the Dashboard Screen
            Dashboard_Scr.Update_EarningsBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

class TransactionInPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        ItemName = list(self.itemToMod.keys())[0]
        self.ids["DataValue"].text = str(self.itemToMod[ItemName][0])
        self.ids["AmountValue"].text = str(self.itemToMod[ItemName][1])
        self.ids["CategoryValue"].text = str(self.itemToMod[ItemName][2])
        self.ids["PaidWith"].text = str(self.itemToMod[ItemName][4])
        self.ids["DescriptionValue"].text = str(self.itemToMod[ItemName][3])
        pass

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Data Category" from Text Input - In empty do nothing
        DataValue = self.ids["DataValue"].text.strip()
        if not DataValue: string = string + 'ERROR: Empty data FIELD\n'

        # Retrive data "Amount Value" from Text Input - In empty do nothing
        AmountValue = self.ids["AmountValue"].text.strip()
        if not AmountValue: string = string + 'ERROR: Empty amount value FIELD\n'
        if not AmountValue.replace(".", "").isnumeric(): string = string + 'ERROR: Amount value must be numeric FIELD\n'

        # Retrive data "CategoryValue" from Text Input - In empty do nothing
        CategoryValue = self.ids["CategoryValue"].text.strip()
        if not CategoryValue: string = string + 'ERROR: Empty category FIELD\n'
        
        # Retrive data "PaidWith" from Text Input - In empty do nothing
        PaidWith = self.ids["PaidWith"].text.strip()
        if not PaidWith: string = string + 'ERROR: Empty Paid with FIELD\n'
        
        # Retrive data "DescriptionValue" from Text Input - In empty do nothing
        DescriptionValue = self.ids["DescriptionValue"].text.strip()

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            Transaction_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].TransactionIn_DBManager
            New_Element = [DataValue, AmountValue, CategoryValue, DescriptionValue, PaidWith]

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElementList(ItemNum = list(self.itemToMod.keys())[0], NewList = New_Element)
                pass

            else:
                # Append new item
                Json_mng.ConcatenateElementList(New_Element)

            # Update the Json and Update the Dashboard Screen
            Transaction_Scr.Update_TransactionInBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

class TransactionOutPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title_str, size_hint=(0.3,0.5))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        ItemName = list(self.itemToMod.keys())[0]
        self.ids["DataValue"].text = str(self.itemToMod[ItemName][0])
        self.ids["AmountValue"].text = str(self.itemToMod[ItemName][1])
        self.ids["CategoryValue"].text = str(self.itemToMod[ItemName][2])
        self.ids["PaidWith"].text = str(self.itemToMod[ItemName][4])
        self.ids["DescriptionValue"].text = str(self.itemToMod[ItemName][3])
        pass

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Data Category" from Text Input - In empty do nothing
        DataValue = self.ids["DataValue"].text.strip()
        if not DataValue: string = string + 'ERROR: Empty data FIELD\n'

        # Retrive data "Amount Value" from Text Input - In empty do nothing
        AmountValue = self.ids["AmountValue"].text.strip()
        if not AmountValue: string = string + 'ERROR: Empty amount value FIELD\n'
        if not AmountValue.replace(".", "").isnumeric(): string = string + 'ERROR: Amount value must be numeric FIELD\n'

        # Retrive data "CategoryValue" from Text Input - In empty do nothing
        CategoryValue = self.ids["CategoryValue"].text.strip()
        if not CategoryValue: string = string + 'ERROR: Empty category FIELD\n'
        
        # Retrive data "PaidWith" from Text Input - In empty do nothing
        PaidWith = self.ids["PaidWith"].text.strip()
        if not PaidWith: string = string + 'ERROR: Empty Paid with FIELD\n'
        
        # Retrive data "DescriptionValue" from Text Input - In empty do nothing
        DescriptionValue = self.ids["DescriptionValue"].text.strip()

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            Transaction_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].TransactionOut_DBManager
            New_Element = [DataValue, AmountValue, CategoryValue, DescriptionValue, PaidWith]

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElementList(ItemNum = list(self.itemToMod.keys())[0], NewList = New_Element)
                pass

            else:
                # Append new item
                Json_mng.ConcatenateElementList(New_Element)

            # Update the Json and Update the Dashboard Screen
            Transaction_Scr.Update_TransactionOutBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

    def __init__(self, title = '', type = 'A', itemToMod = {}):
        # Initialize the super class
        super().__init__(title = title, size_hint=(0.2,0.3))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        ItemName = list(self.itemToMod.keys())[0]
        self.ids["NameValue"].text = ItemName
        self.ids["SymbolValue"].text = str(self.itemToMod[ItemName][0])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Name Value" from Text Input - In empty do nothing
        NameValue = self.ids["NameValue"].text.strip()
        if not NameValue: string = string + 'ERROR: Empty Name FIELD\n'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + 'ERROR: Empty last month value FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            Crypto_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].CryptoAssets_DBManager
            New_Element = Crypto_Scr.Compute_CryptoAssetsList(NameValue, SymbolValue)
            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElement(Old_element = self.itemToMod, New_Item = New_Element)
            else:
                # Append new item
                Json_mng.AddElement(New_Element)

            # Update the Json and Update the Dashboard Screen
            Crypto_Scr.Update_CryptoAssetsList()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()