from kivy.core.window import Window

#-- maximize first, to get the screen size, minus any OS toolbars
class WindowInfos():
    def __init__(self):
        Window.maximize()
        self.maxSize = Window.system_size
        self.desiredSize_x = self.maxSize[0]*0.9
        self.desiredSize_y = self.maxSize[1]*0.9
        self.left = (self.maxSize[0] -self.desiredSize_x)*0.5
        self.top = (self.maxSize[1] - self.desiredSize_y)*0.5

#-- set the actual window size, to be slightly smaller than full screen
def SetWindowSize():
    Win = WindowInfos()
    Window.size = (Win.desiredSize_x, Win.desiredSize_y)
    Window.minimum_width = Win.desiredSize_x
    Window.minimum_height =  Win.desiredSize_y
    Window.left = Win.left
    Window.top = Win.top