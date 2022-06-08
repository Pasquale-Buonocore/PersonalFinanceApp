from kivy.uix.screenmanager import Screen
from Packages.CustomFunction.CustomFunction import ReturnJsonPathGivenScreenName

class AssetsScreen(Screen):

    def UpdateScreen(self, FromScreenName, PortfolioName):
        # Save the father name
        self.FromScreenName = FromScreenName
        self.PortfolioName = PortfolioName

        # Update the Label of the String
        self.ids['FirstRowLabel'].text = 'ASSETS IN ' + self.PortfolioName.upper() + ' PORTFOLIO [' + self.FromScreenName.upper() + ']'

    def ReturnBack(self):
        print('Returnig back to ' + self.FromScreenName)
        ScreenManager = self.parent
        ScreenManager.current = 'PORTFOLIO'
        ScreenManager.current_screen.UpdateScreen(ScreenName = self.FromScreenName, PortfolioJsonPath = ReturnJsonPathGivenScreenName(self.FromScreenName))