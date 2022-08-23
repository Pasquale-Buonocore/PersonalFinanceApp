from kivy.lang import Builder
from kivymd.app import MDApp
from DataPickerItem import MDDatePicker
import datetime as dt

class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Light"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file('data_picker_test.kv')

	# Click OK
	def on_save(self, instance, value, date_range):
		#print(instance, value, date_range)
		#self.root.ids.date_label.text = str(value)
		self.root.ids.date_label.text = dt.date(value.year, value.month, value.day).strftime("%d %B %Y")

	# Click Cancel
	def on_cancel(self, instance, value):
		self.root.ids.date_label.text = "You Clicked Cancel"


	def show_date_picker(self):
		#date_dialog = MDDatePicker(year=2000, month=2, day=14)
		date_dialog = MDDatePicker(mode="picker")
		date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
		date_dialog.open()
	
	
MainApp().run()