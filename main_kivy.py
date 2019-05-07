
# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS	                              //
# ////////////////////////////////////////////////////////////////
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
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

sm = ScreenManager()

class MyApp(App):
    
    def build(self):
        return sm


#Load all the KV Files
Builder.load_file('sand_table.kv')

class MainScreen(Screen):

    def next(self):
        print('hi')
        
mainscreen = MainScreen(name = 'mainscreen')
sm.add_widget(mainscreen)

sm.current = 'mainscreen'

if __name__ == '__main__':
    
    MyApp().run()