from kivy.lang import Builder
from kivymd.app import MDApp
from Packages.CustomItem.DataPicker.DataPickerItem import MDDatePicker
import datetime as dt

class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Light"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file('data_picker_test.kv')

	# Click OK
	def on_save(self, instance, value, date_range):
		self.root.ids.date_label.text = dt.date(value.year, value.month, value.day).strftime("%d %B %Y")

	def show_date_picker(self, date):
		#date_dialog = MDDatePicker(year=2000, month=2, day=14)
		date_dialog = MDDatePicker(mode="picker", primary_color= [0.3, 0.3, 0.5, 1], year = date.year, month = date.month, day = date.day)
		date_dialog.bind(on_save=self.on_save)
		date_dialog.open()
	
	
MainApp().run()