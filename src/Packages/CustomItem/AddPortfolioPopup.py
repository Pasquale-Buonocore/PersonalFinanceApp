from kivy.lang import Builder
from kivy.uix.popup import Popup

# Designate Out .kv design file
Builder.load_file('ui/AddPortfolioPopup.kv')

class AddPortfolioPopup(Popup):
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