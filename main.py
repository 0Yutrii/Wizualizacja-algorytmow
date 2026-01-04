from kivy.config import Config
#wczytywanie z pliku???
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Config.set('graphics', 'borderless', '0')
Config.set('graphics', 'resizable', '1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from wizualizacja_pso import WizualizacjaAlgorytmow

Builder.load_file("Wizualizacja.kv")

class StartScreen(Screen):
    
    pass

class MyScreenManager(ScreenManager):
    pass

class Wizualizacja(App):
    def build(self):
        sm = ScreenManager()
        #sm.add_widget(StartScreen(name="Start"))
        sm.add_widget(WizualizacjaAlgorytmow(name="Particle Swarm Optimization"))
        #self.fps = klasa1.FPSmeter()
        #Clock.schedule_once(lambda dt: self.fps.start(), 0)  
        return sm


if __name__ == '__main__':
    Wizualizacja().run()