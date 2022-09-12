import Packages.CustomItem.Popup.WarningPopup as Wrn_popup
from kivy.uix.popup import Popup
from kivy.lang import Builder
import re

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/AddTransactionClassPopup.kv')

class AddTransactionClassPopup(Popup):
    def __init__(self, direction, itemToMod = {}):
        # Initialize the super class
        super().__init__(title = 'ADD TRANSACTION ' + direction + ' CLASS', size_hint = (0.3,0.5))

        # Define inner attributes
        self.direction = direction

    def Confirm(self, App):
        # Keep the boolean error
        string = ''

        # Retrive data "Class Name" from Text Input - In empty do nothing
        ClassName = self.ids["ClassName"].text.strip()
        if not ClassName: string = string + 'ERROR: Empty Class name FIELD'

        # Retrive data "Desired Value" from Text Input - In empty do nothing
        DesiredValue = self.ids["DesiredValue"].text.strip()
        if not DesiredValue: string = string + '\nERROR: Empty desired allocation value FIELD'

        if string:
            # If the error message is not empty, display an error
            Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
            Pop.open()
        else:
            # Instantiate Screen and Json manager
            ActualScreen = App.root.children[0].children[0].children[0]
            DBManager = ActualScreen.TransactionIn if self.direction == 'IN' else ActualScreen.TransactionOut

            # Check first if the actual class name already exist
            if ClassName in DBManager.ReadJson()[self.direction]['Assets'].keys():
                # If the error message is not empty, display an error
                string = ClassName + ' transaction class already exists.\nAdd a different one if you need!'
                Pop = Wrn_popup.WarningPopup('WARNING WINDOW', string.upper())
                Pop.open()

            # Otherwise add it to the portfolio, update the popup and Screen
            else:

                # Define Portfolio To Add
                NewTransactionClassToAdd = DBManager.InitializeNewTransactionAsset(ClassName)
                
                # Add to DB and update desired allocation
                DBManager.AddAssetToPortfolio(self.direction, NewTransactionClassToAdd)
                DBManager.UpdatePortfolioDesiredAssetAllocation(self.direction, {ClassName: int(re.sub('\D','', DesiredValue))})
                DBManager.UpdatePortfolioActualAssetAllocation(self.direction)
               
                # Update the opened popup
                self.parent.children[1].PopulateListOfClasses()

                # Update the Transaction Screen
                ActualScreen.UpdateScreen()

                # Close the actual Popup
                self.dismiss()

    def Cancel(self):
        # Close the popup
        self.dismiss()