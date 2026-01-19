from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from kivy.uix.popup import Popup
from kivy.properties import ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.lang import Builder
from kivy.factory import Factory

from functools import partial


import numpy as np

# from utils import resource_path
# Builder.load_file(
#     str(resource_path("settings/pso_settings_menu.kv"))
# )

class PsoSettingsMenu(Popup):
    point = ObjectProperty(None)
    callback_apply = ObjectProperty(None)
    data = ListProperty(None)
    temp_swarm_size = None
    temp_plot_range = None
    temp_math_fun = None

    def on_open(self):
        self.temp_plot_range = self.data[0]
        self.temp_swarm_size = self.data[1]
        self.temp_math_fun = self.data[2]

        sliders_swarm_map = {
            "w": self.ids.sliderW,
            "c1": self.ids.sliderC1,
            "c2": self.ids.sliderC2,
            "v_max": self.ids.sliderVmax,
        }
        sliders_plot_map ={
            "swarmSize": self.ids.sliderSwarmSize
        }
        
        range_input_map = {
            0: self.ids.inputMinX,
            1: self.ids.inputMaxX,
            2: self.ids.inputMinY,
            3: self.ids.inputMaxY
        }
        for number,range_input in range_input_map.items():
            range_input.text = str(self.temp_plot_range[number])


        if self.point is not None:
            try:
                self.ids.sliderW.value = float(self.point.w)
                self.ids.sliderC1.value = float(self.point.c1)
                self.ids.sliderC2.value = float(self.point.c2)
                self.ids.sliderVmax.value = float(self.point.v_max) 
                self.ids.sliderSwarmSize.value = int(self.temp_swarm_size)
            except Exception:
                pass
         
        for name, slider in sliders_swarm_map.items():
            slider.bind(value=partial(self._on_swarm_slider_change, name))

        
        

    def _on_swarm_slider_change(self, name, slider, value):
        
        if self.point is None:
            return
        
        setattr(self.point, name, value)
        #print(f"OptionsMenu: set {name} = {value:.2f} on {self.point}")


    def _function_choice(self,number):
        range_input_map = {
            1: [-6.0,6.0,-6.0,6.0],
            2: [-2.0,2.0,-1.0,3.0],
            3: [-5.12,5.12,-5.12,5.12],
            4: [-5.0,5.0,-5.0,5.0]
        }
        
        self.temp_plot_range = range_input_map.get(number)
        self.temp_math_fun = number
        self._set_range_input_values()
        

    def _validate_range(self,instance):
        try:
            self.temp_plot_range[0] = np.clip(float(self.ids.inputMinX.text),-10,9)
            self.temp_plot_range[1] = np.clip(float(self.ids.inputMaxX.text),-9,10)
            self.temp_plot_range[2] = np.clip(int(self.ids.inputMinY.text),-10,9)
            self.temp_plot_range[3] = np.clip(int(self.ids.inputMaxY.text),-9,10)
        except ValueError:
            return 
        
        self.temp_plot_range = np.array(self.temp_plot_range).tolist()
        
        if self.temp_plot_range[0] == self.temp_plot_range[1]:
            self.temp_plot_range[1] = self.temp_plot_range[1]-1
        
        if self.temp_plot_range[2] == self.temp_plot_range[3]:
            self.temp_plot_range[3] = self.temp_plot_range[3]-1

        if self.temp_plot_range[0] > self.temp_plot_range[1]:
            self.temp_plot_range[0],self.temp_plot_range[1] = self.temp_plot_range[1], self.temp_plot_range[0]
        
        if self.temp_plot_range[2] > self.temp_plot_range[3]:
            self.temp_plot_range[2],self.temp_plot_range[3] = self.temp_plot_range[3], self.temp_plot_range[2]

        self._set_range_input_values()

        
    def _set_range_input_values(self):
        self.ids.inputMinX.text = str(self.temp_plot_range[0])
        self.ids.inputMaxX.text = str(self.temp_plot_range[1])
        self.ids.inputMinY.text = str(self.temp_plot_range[2])
        self.ids.inputMaxY.text = str(self.temp_plot_range[3])

    def _on_apply(self,instance):
        self.callback_apply(self.temp_plot_range,self.temp_swarm_size, self.temp_math_fun)
        
    
    # def _on_save(self, instance):
    
    #     if self.point:
    #         print("Saving:", self.point)


    # def _on_load(self, instance):
    
    #     print("Load requested")
        

    

    