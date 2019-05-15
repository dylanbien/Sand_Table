
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

    def run(self, str):
        sm.get_screen('mainscreen').ids.Status.text='Making Design: ' + str
        if str == 'inward spiral':
            pass
            #Clock.schedule_once(lambda _: motors.spiral('in'), 0)
        if str == 'outward spiral':
            Clock.schedule_once(lambda _: motors.spiral('out'), 0)
        if str == 'overlapping triangle':
            Clock.schedule_once(lambda _: motors.make_shape_same('outward',3, False), 0)
        if str == 'overlapping pentagon':
            Clock.schedule_once(lambda _: motors.make_shape_same('outward', 5), 0)
        if str == 'inward triangle':
            Clock.schedule_once(lambda _: motors.make_shape_same('inward', 3), 0)
        if str == 'outward triangle':
            Clock.schedule_once(lambda _: motors.make_shape_same('outward', 3), 0)
        if str == 'inward square':
            Clock.schedule_once(lambda _: motors.make_shape_same('inward', 4), 0)
        if str == 'outward square':
            Clock.schedule_once(lambda _: motors.make_shape_same('outward', 4), 0)
        if str == 'outward hexagon':
            Clock.schedule_once(lambda _: motors.make_shape_same('outward', 6), 0)
        if str == 'inward hexagon':
            Clock.schedule_once(lambda _: motors.make_shape_same('inward', 6), 0)
        if str == 'sinusoidal':
            Clock.schedule_once(lambda _: motors.sinusoidal(-100000, 'out'), 0)
        if str == 'flower':
            Clock.schedule_once(lambda _: motors.flower(-100000, 5), 0)
            
        Clock.schedule_once(lambda _: self.reset_screen, 0)

    def reset_screen(self):
        sm.get_screen('mainscreen').ids.Status.text='Status: Ready'
    
mainscreen = MainScreen(name = 'mainscreen')
sm.add_widget(mainscreen)

sm.current = 'mainscreen'

if __name__ == '__main__':
    MyApp().run()
