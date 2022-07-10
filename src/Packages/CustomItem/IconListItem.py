from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivy.lang import Builder

# Designate Out .kv design file
Builder.load_file('Packages/CustomItem/ui/IconListItem.kv')

class IconListItem(OneLineIconListItem):
    icon = StringProperty()