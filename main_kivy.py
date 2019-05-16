
# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS	    //
# ////////////////////////////////////////////////////////////////

import os
os.environ['KIVY_WINDOW'] = 'egl_rpi'
#egl_rpi only works with monitor (sdl2 for both)

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
from time import sleep
import motor_setup
'''
import Adafruit_Ease_Lib_Sand_Table

leds = Adafruit_Ease_Lib_Sand_Table.Adafruit_Ease_Lib()

leds.change_frequency(2000)

from threading import Thread
t = Thread(target = leds.run_lights)
t.start()
#disable touch
'''
motors = motor_setup.motor_setup()
sleep(1)
motors.prepare_table()

sm = ScreenManager()

class MyApp(App):
    def build(self):
        return sm


#Load all the KV Files
Builder.load_file('sand_table.kv')


class MainScreen(Screen):
    def next(self):
        print('hi')
    def run(self,str):
        self.disable_buttons()
        sm.get_screen('mainscreen').ids.Status.text='Making Design: ' + str
        Clock.schedule_once(lambda _: self.move_motors(str), 0)
        
    def move_motors(self, str):
        
        if str == 'inward spiral':
            pass
            #motors.spiral('in')
        if str == 'outward spiral':
            motors.spiral('out')
        if str == 'overlapping triangle':
            motors.make_shape_same('outward',3, False)
        if str == 'overlapping pentagon':
            motors.make_shape_same('outward', 5)
        if str == 'inward triangle':
            motors.make_shape_same('inward', 3)
        if str == 'outward triangle':
            motors.make_shape_same('outward', 3)
        if str == 'inward square':
            motors.make_shape_same('inward', 4)
        if str == 'outward square':
            motors.make_shape_same('outward', 4)
        if str == 'outward hexagon':
            motors.make_shape_same('outward', 6)
        if str == 'inward hexagon':
            motors.make_shape_same('inward', 6)
        if str == 'sinusoidal':
            motors.sinusoidal(-100000, 'out')
        if str == 'flower':
            motors.flower(-100000, 5)
            
        sm.get_screen('mainscreen').ids.Status.text='Status: Ready'
        self.enable_buttons()
        
        
    def disable_buttons(self):
        self.ids.button1.disabled = True
        self.ids.button2.disabled = True
        self.ids.button3.disabled = True
        self.ids.button4.disabled = True
        self.ids.button5.disabled = True
        self.ids.button6.disabled = True
        self.ids.button7.disabled = True
        self.ids.button8.disabled = True
        self.ids.button9.disabled = True
        self.ids.button10.disabled = True
        self.ids.button11.disabled = True
        self.ids.button12.disabled = True
        
    def enable_buttons(self):
        self.ids.button1.disabled = False
        self.ids.button2.disabled = False
        self.ids.button3.disabled = False
        self.ids.button4.disabled = False
        self.ids.button5.disabled = False
        self.ids.button6.disabled = False
        self.ids.button7.disabled = False
        self.ids.button8.disabled = False
        self.ids.button9.disabled = False
        self.ids.button10.disabled = False
        self.ids.button11.disabled = False
        self.ids.button12.disabled = False

    
mainscreen = MainScreen(name = 'mainscreen')
sm.add_widget(mainscreen)

sm.current = 'mainscreen'

if __name__ == '__main__':
    MyApp().run()
