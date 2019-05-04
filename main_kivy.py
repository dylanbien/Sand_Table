import ODrive_Ease_Lib
import motor_setup
import Adafruit_Ease_Lib_Sand_Table
from time import sleep

# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS	                              //
# ////////////////////////////////////////////////////////////////
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix import togglebutton
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
from kivy.properties import StringProperty
from time import sleep
Window.fullscreen = True
sm = ScreenManager()

class MyApp(App):
	def build(self):
	  return sm


#Load all the KV Files
Builder.load_file('sand_table.kv')


motors = motor_setup.motor_setup()
sleep(1)
motors.prepare_table()

if __name__ == "__main__":
        MyApp().run()
