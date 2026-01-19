from kivy.config import Config

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Config.set('graphics', 'borderless', '0')
Config.set('graphics', 'resizable', '1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from wizualizacja_pso import PSOScreen
from ant_colony import AntColonyScreen

import sys
from pathlib import Path

#from logic.utils import resource_path

#Builder.load_file(str(resource_path("Wizualizacja.kv")))

class StartScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass


class WizualizacjaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="Start"))
        sm.add_widget(PSOScreen(name="Particle_Swarm_Optimization"))
        sm.add_widget(AntColonyScreen(name="Ant_Colony"))
        
        return sm


if __name__ == '__main__':
    WizualizacjaApp().run()