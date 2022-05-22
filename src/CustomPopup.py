from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
import DatabaseMng as db_manager
from kivy.uix.modalview import ModalView

# Designate Out .kv design file
Builder.load_file('ui/PopupMng.kv')

class WarningPopup(Popup):
    def __init__(self, title_str, message):
        self.MessageToDisplay = message
        super().__init__(title = title_str, size_hint=(0.25,0.3))

class RemovingPopup(Popup):
    def __init__(self, ManagerOfItem, ManagerOfScreen, DBManager, UpdateFunction_str, RemoveFunction = 'RemoveElement',title_str = 'REMOVING WARNING'):
        super().__init__(title = title_str, size_hint=(0.25,0.2))
        self.ManagerOfItem = ManagerOfItem
        self.ManagerOfScreen = ManagerOfScreen
        self.DBManager = DBManager
        self.UpdateFunction_str = UpdateFunction_str
        self.RemoveFunction_str = RemoveFunction

    def RemoveIt(self):
        # When the remove button is pressed, the item should be removed from the json. The UI shall be updated as well.
        # Remove widget from the Json
        getattr(self.DBManager, self.RemoveFunction_str)(self.ManagerOfItem)
        # Update the UI
        getattr(self.ManagerOfScreen, self.UpdateFunction_str)()
        # Close the popup
        self.dismiss()

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
            Pop = WarningPopup('', string.upper())
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
            Pop = WarningPopup('', string.upper())
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
            Pop = WarningPopup('', string.upper())
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
            Pop = WarningPopup('', string.upper())
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
            Pop = WarningPopup('', string.upper())
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

class ETF_ETCPopup(Popup):
    def __init__(self, title_str, type, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = 'Add Transaction', size_hint=(0.3,0.7))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        ItemName = list(self.itemToMod.keys())[0]
        self.ids["NameValue"].text = str(self.itemToMod[ItemName][0])
        self.ids["SymbolValue"].text = str(self.itemToMod[ItemName][1])
        self.ids["DataValue"].text = str(self.itemToMod[ItemName][2])
        self.ids["TypeValue"].text = str(self.itemToMod[ItemName][3])
        self.ids["BrokerValue"].text = str(self.itemToMod[ItemName][4])
        self.ids["QuantityValue"].text = str(self.itemToMod[ItemName][5])
        self.ids["SinglePriceValue"].text = str(self.itemToMod[ItemName][6])


    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Asset Name Value" from Text Input - In empty do nothing
        NameValue = self.ids["NameValue"].text.strip()
        if not NameValue: string = string + 'ERROR: Empty asset name FIELD\n'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + 'ERROR: Empty symbol value FIELD\n'

        # Retrive data "DataValue" from Text Input - In empty do nothing
        DataValue = self.ids["DataValue"].text.strip()
        if not DataValue: string = string + 'ERROR: Empty data FIELD\n'
        
        # Retrive data "TypeValue" from Text Input - In empty do nothing
        TypeValue = self.ids["TypeValue"].text.strip()
        if not TypeValue: string = string + 'ERROR: Empty Type value FIELD\n'
        
        # Retrive data "BrokerValue" from Text Input - In empty do nothing
        BrokerValue = self.ids["BrokerValue"].text.strip()
        if not BrokerValue: string = string + 'ERROR: Empty Broker value FIELD\n'
        
        # Retrive data "QuantityValue" from Text Input - In empty do nothing
        QuantityValue = self.ids["QuantityValue"].text.strip()
        if not QuantityValue: string = string + 'ERROR: Empty Quantity value FIELD\n'
        if not QuantityValue.replace(".", "").isnumeric(): string = string + 'ERROR: Quantity value must be numeric FIELD\n'

        # Retrive data "SinglePriceValue" from Text Input - In empty do nothing
        SinglePriceValue = self.ids["SinglePriceValue"].text.strip()
        if not SinglePriceValue: string = string + 'ERROR: Empty single price value FIELD\n'
        if not SinglePriceValue.replace(".", "").isnumeric(): string = string + 'ERROR: Single price value must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = WarningPopup('', string.upper())
            Pop.open()
        else:
            # Compute total spent
            Total_Spent = float(QuantityValue) * float(SinglePriceValue)

            # Instantiate Dashboard Screen and Json manager
            ETF_ETC_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].ETF_ETC_DBManager
            New_Element = [NameValue, SymbolValue, DataValue, TypeValue, BrokerValue, QuantityValue, SinglePriceValue, Total_Spent]

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElementList(ItemNum = list(self.itemToMod.keys())[0], NewList = New_Element)
            else:
                # Append new item
                Json_mng.ConcatenateElementList(New_Element)

            # Update the Json and Update the Dashboard Screen
            ETF_ETC_Scr.Update_ETF_ETCBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

class StocksPopup(Popup):
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
        self.ids["NameValue"].text = str(self.itemToMod[ItemName][0])
        self.ids["SymbolValue"].text = str(self.itemToMod[ItemName][1])
        self.ids["DataValue"].text = str(self.itemToMod[ItemName][2])
        self.ids["TypeValue"].text = str(self.itemToMod[ItemName][3])
        self.ids["BrokerValue"].text = str(self.itemToMod[ItemName][4])
        self.ids["QuantityValue"].text = str(self.itemToMod[ItemName][5])
        self.ids["SinglePriceValue"].text = str(self.itemToMod[ItemName][6])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Asset Name Value" from Text Input - In empty do nothing
        NameValue = self.ids["NameValue"].text.strip()
        if not NameValue: string = string + 'ERROR: Empty asset name FIELD\n'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + 'ERROR: Empty symbol value FIELD\n'

        # Retrive data "DataValue" from Text Input - In empty do nothing
        DataValue = self.ids["DataValue"].text.strip()
        if not DataValue: string = string + 'ERROR: Empty data FIELD\n'
        
        # Retrive data "TypeValue" from Text Input - In empty do nothing
        TypeValue = self.ids["TypeValue"].text.strip()
        if not TypeValue: string = string + 'ERROR: Empty Type value FIELD\n'
        
        # Retrive data "BrokerValue" from Text Input - In empty do nothing
        BrokerValue = self.ids["BrokerValue"].text.strip()
        if not BrokerValue: string = string + 'ERROR: Empty Broker value FIELD\n'
        
        # Retrive data "QuantityValue" from Text Input - In empty do nothing
        QuantityValue = self.ids["QuantityValue"].text.strip()
        if not QuantityValue: string = string + 'ERROR: Empty Quantity value FIELD\n'
        if not QuantityValue.replace(".", "").isnumeric(): string = string + 'ERROR: Quantity value must be numeric FIELD\n'

        # Retrive data "SinglePriceValue" from Text Input - In empty do nothing
        SinglePriceValue = self.ids["SinglePriceValue"].text.strip()
        if not SinglePriceValue: string = string + 'ERROR: Empty single price value FIELD\n'
        if not SinglePriceValue.replace(".", "").isnumeric(): string = string + 'ERROR: Single price value must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = WarningPopup('', string.upper())
            Pop.open()
        else:
            # Compute total spent
            Total_Spent = float(QuantityValue) * float(SinglePriceValue)

            # Instantiate Dashboard Screen and Json manager
            Stocks_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].Stocks_DBManager
            New_Element = [NameValue, SymbolValue, DataValue, TypeValue, BrokerValue, QuantityValue, SinglePriceValue, Total_Spent]

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElementList(ItemNum = list(self.itemToMod.keys())[0], NewList = New_Element)
            else:
                # Append new item
                Json_mng.ConcatenateElementList(New_Element)

            # Update the Json and Update the Dashboard Screen
            Stocks_Scr.Update_StocksBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

class BondsPopup(Popup):
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
        self.ids["NameValue"].text = str(self.itemToMod[ItemName][0])
        self.ids["SymbolValue"].text = str(self.itemToMod[ItemName][1])
        self.ids["DataValue"].text = str(self.itemToMod[ItemName][2])
        self.ids["TypeValue"].text = str(self.itemToMod[ItemName][3])
        self.ids["BrokerValue"].text = str(self.itemToMod[ItemName][4])
        self.ids["QuantityValue"].text = str(self.itemToMod[ItemName][5])
        self.ids["SinglePriceValue"].text = str(self.itemToMod[ItemName][6])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Asset Name Value" from Text Input - In empty do nothing
        NameValue = self.ids["NameValue"].text.strip()
        if not NameValue: string = string + 'ERROR: Empty asset name FIELD\n'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + 'ERROR: Empty symbol value FIELD\n'

        # Retrive data "DataValue" from Text Input - In empty do nothing
        DataValue = self.ids["DataValue"].text.strip()
        if not DataValue: string = string + 'ERROR: Empty data FIELD\n'
        
        # Retrive data "TypeValue" from Text Input - In empty do nothing
        TypeValue = self.ids["TypeValue"].text.strip()
        if not TypeValue: string = string + 'ERROR: Empty Type value FIELD\n'
        
        # Retrive data "BrokerValue" from Text Input - In empty do nothing
        BrokerValue = self.ids["BrokerValue"].text.strip()
        if not BrokerValue: string = string + 'ERROR: Empty Broker value FIELD\n'
        
        # Retrive data "QuantityValue" from Text Input - In empty do nothing
        QuantityValue = self.ids["QuantityValue"].text.strip()
        if not QuantityValue: string = string + 'ERROR: Empty Quantity value FIELD\n'
        if not QuantityValue.replace(".", "").isnumeric(): string = string + 'ERROR: Quantity value must be numeric FIELD\n'

        # Retrive data "SinglePriceValue" from Text Input - In empty do nothing
        SinglePriceValue = self.ids["SinglePriceValue"].text.strip()
        if not SinglePriceValue: string = string + 'ERROR: Empty single price value FIELD\n'
        if not SinglePriceValue.replace(".", "").isnumeric(): string = string + 'ERROR: Single price value must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = WarningPopup('', string.upper())
            Pop.open()
        else:
            # Compute total spent
            Total_Spent = float(QuantityValue) * float(SinglePriceValue)

            # Instantiate Dashboard Screen and Json manager
            Bonds_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].Bonds_DBManager
            New_Element = [NameValue, SymbolValue, DataValue, TypeValue, BrokerValue, QuantityValue, SinglePriceValue, Total_Spent]

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElementList(ItemNum = list(self.itemToMod.keys())[0], NewList = New_Element)
            else:
                # Append new item
                Json_mng.ConcatenateElementList(New_Element)

            # Update the Json and Update the Dashboard Screen
            Bonds_Scr.Update_BondsBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

class CommoditiesPopup(Popup):
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
        self.ids["NameValue"].text = str(self.itemToMod[ItemName][0])
        self.ids["SymbolValue"].text = str(self.itemToMod[ItemName][1])
        self.ids["DataValue"].text = str(self.itemToMod[ItemName][2])
        self.ids["TypeValue"].text = str(self.itemToMod[ItemName][3])
        self.ids["BrokerValue"].text = str(self.itemToMod[ItemName][4])
        self.ids["QuantityValue"].text = str(self.itemToMod[ItemName][5])
        self.ids["SinglePriceValue"].text = str(self.itemToMod[ItemName][6])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Asset Name Value" from Text Input - In empty do nothing
        NameValue = self.ids["NameValue"].text.strip()
        if not NameValue: string = string + 'ERROR: Empty asset name FIELD\n'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + 'ERROR: Empty symbol value FIELD\n'

        # Retrive data "DataValue" from Text Input - In empty do nothing
        DataValue = self.ids["DataValue"].text.strip()
        if not DataValue: string = string + 'ERROR: Empty data FIELD\n'
        
        # Retrive data "TypeValue" from Text Input - In empty do nothing
        TypeValue = self.ids["TypeValue"].text.strip()
        if not TypeValue: string = string + 'ERROR: Empty Type value FIELD\n'
        
        # Retrive data "BrokerValue" from Text Input - In empty do nothing
        BrokerValue = self.ids["BrokerValue"].text.strip()
        if not BrokerValue: string = string + 'ERROR: Empty Broker value FIELD\n'
        
        # Retrive data "QuantityValue" from Text Input - In empty do nothing
        QuantityValue = self.ids["QuantityValue"].text.strip()
        if not QuantityValue: string = string + 'ERROR: Empty Quantity value FIELD\n'
        if not QuantityValue.replace(".", "").isnumeric(): string = string + 'ERROR: Quantity value must be numeric FIELD\n'

        # Retrive data "SinglePriceValue" from Text Input - In empty do nothing
        SinglePriceValue = self.ids["SinglePriceValue"].text.strip()
        if not SinglePriceValue: string = string + 'ERROR: Empty single price value FIELD\n'
        if not SinglePriceValue.replace(".", "").isnumeric(): string = string + 'ERROR: Single price value must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = WarningPopup('', string.upper())
            Pop.open()
        else:
            # Compute total spent
            Total_Spent = float(QuantityValue) * float(SinglePriceValue)

            # Instantiate Dashboard Screen and Json manager
            Commodities_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].Commodities_DBManager
            New_Element = [NameValue, SymbolValue, DataValue, TypeValue, BrokerValue, QuantityValue, SinglePriceValue, Total_Spent]

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElementList(ItemNum = list(self.itemToMod.keys())[0], NewList = New_Element)
            else:
                # Append new item
                Json_mng.ConcatenateElementList(New_Element)

            # Update the Json and Update the Dashboard Screen
            Commodities_Scr.Update_CommoditiesBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

class CryptoPopup(Popup):
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
        self.ids["NameValue"].text = str(self.itemToMod[ItemName][0])
        self.ids["SymbolValue"].text = str(self.itemToMod[ItemName][1])
        self.ids["DataValue"].text = str(self.itemToMod[ItemName][2])
        self.ids["TypeValue"].text = str(self.itemToMod[ItemName][3])
        self.ids["BrokerValue"].text = str(self.itemToMod[ItemName][4])
        self.ids["QuantityValue"].text = str(self.itemToMod[ItemName][5])
        self.ids["SinglePriceValue"].text = str(self.itemToMod[ItemName][6])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Asset Name Value" from Text Input - In empty do nothing
        NameValue = self.ids["NameValue"].text.strip()
        if not NameValue: string = string + 'ERROR: Empty asset name FIELD\n'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + 'ERROR: Empty symbol value FIELD\n'

        # Retrive data "DataValue" from Text Input - In empty do nothing
        DataValue = self.ids["DataValue"].text.strip()
        if not DataValue: string = string + 'ERROR: Empty data FIELD\n'
        
        # Retrive data "TypeValue" from Text Input - In empty do nothing
        TypeValue = self.ids["TypeValue"].text.strip()
        if not TypeValue: string = string + 'ERROR: Empty Type value FIELD\n'
        
        # Retrive data "BrokerValue" from Text Input - In empty do nothing
        BrokerValue = self.ids["BrokerValue"].text.strip()
        if not BrokerValue: string = string + 'ERROR: Empty Broker value FIELD\n'
        
        # Retrive data "QuantityValue" from Text Input - In empty do nothing
        QuantityValue = self.ids["QuantityValue"].text.strip()
        if not QuantityValue: string = string + 'ERROR: Empty Quantity value FIELD\n'
        if not QuantityValue.replace(".", "").isnumeric(): string = string + 'ERROR: Quantity value must be numeric FIELD\n'

        # Retrive data "SinglePriceValue" from Text Input - In empty do nothing
        SinglePriceValue = self.ids["SinglePriceValue"].text.strip()
        if not SinglePriceValue: string = string + 'ERROR: Empty single price value FIELD\n'
        if not SinglePriceValue.replace(".", "").isnumeric(): string = string + 'ERROR: Single price value must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = WarningPopup('', string.upper())
            Pop.open()
        else:
            # Compute total spent
            Total_Spent = float(QuantityValue) * float(SinglePriceValue)

            # Instantiate Dashboard Screen and Json manager
            Crypto_Scr = App.root.children[0].children[0].children[0]
            Json_mng = App.root.children[0].children[0].children[0].Crypto_DBManager
            New_Element = [NameValue, SymbolValue, DataValue, TypeValue, BrokerValue, QuantityValue, SinglePriceValue, Total_Spent]

            # If an item needs to be modified
            if self.type == 'M':
                # Substitute the actual item
                Json_mng.SubstituteElementList(ItemNum = list(self.itemToMod.keys())[0], NewList = New_Element)
            else:
                # Append new item
                Json_mng.ConcatenateElementList(New_Element)

            # Update the Json and Update the Dashboard Screen
            Crypto_Scr.Update_CryptoBoxLayout()

            # Close the popup
            self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()

#############
# ADD ASSET #
#############
class ETF_ETC_AddAssetPopup(Popup):
    def __init__(self, type = 'A', itemToMod = {}):
        # Initialize the super class
        super().__init__(title = 'ADD ASSET CLASS', size_hint=(0.2,0.3))
        # Define inner attributes
        self.type = type if type in ['A','M'] else 'A'
        # Save item to modify
        self.itemToMod = itemToMod
        # Fill the popup if the user need to modify a field
        if itemToMod: self.ModifyTextInput()

    def ModifyTextInput(self):
        # Modify text input if itemToMod is not empty
        self.ids["NameValue"].text = list(self.itemToMod.keys())[0]
        self.ids["SymbolValue"].text = str(self.itemToMod[self.ids["Location_Input"].text][0])

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Name Value" from Text Input - In empty do nothing
        NameValue = self.ids["NameValue"].text.strip()
        if not NameValue: string = string + 'ERROR: Empty Name FIELD\n'

        # Retrive data "Symbol Value" from Text Input - In empty do nothing
        SymbolValue = self.ids["SymbolValue"].text.strip()
        if not SymbolValue: string = string + 'ERROR: Empty last month value FIELD\n'
        if not SymbolValue.replace(".", "").isnumeric(): string = string + 'ERROR: last month must be numeric FIELD\n'

        if string:
            # If the error message is not empty, display an error
            Pop = WarningPopup('', string.upper())
            Pop.open()
        else:
            # Instantiate Dashboard Screen and Json manager
            ETF_ETC_Scr = App.root.children[0].children[0].children[0]
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
        # Close the popup
        self.dismiss()

class Add_CryptoAssetsPopup(Popup):
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
            Pop = WarningPopup('', string.upper())
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