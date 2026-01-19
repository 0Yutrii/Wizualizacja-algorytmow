

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.core.text import Label as CoreLabel
import numpy as np
from kivy.core.window import Window
from types import MethodType
from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from kivy.clock import Clock

from logic.node import Node
from logic.ant_manager import AntManager
from logic.ant import Ant

import os
import pickle

aglomeracja_slaska = [
    "Katowice",
    "Sosnowiec",
    "Gliwice",
    "Zabrze",
    "Bytom",
    "Ruda Śląska",
    "Tychy",
    "Dąbrowa Górnicza",
    "Chorzów",
    "Jaworzno",
    "Mysłowice",
    "Siemianowice Śląskie",
    "Piekary Śląskie"
]



class GraphWidget(RelativeLayout):
    on_data_change = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.nodes = {}
        self.nodes = self.load_graph()
        
        self.create_node_buttons()
        self.bind(size=self.draw_graph, pos=self.draw_graph)
        self.ant_manager = AntManager(self.nodes,20)
        self.ant_manager.run(iterations=200)
        #self.ant_manager.make_report()

        #self.ant_test(self.nodes["Łódź"])
        #print(self.nodes["Katowice"].name)
        # for i, (name, data) in enumerate(cities.items()):
        #     new_node = Node(name,data['x'],data['y'],data['pop'])
        #     self.nodes[name] = new_node
        # for u,v,lenght in edges:
        #     self.nodes[u].add_neighbor(self.nodes[v],lenght)
        #     self.nodes[v].add_neighbor(self.nodes[u],lenght)  
        # self.ant_test(self.nodes["Szczecin"])
        # for node in self.nodes.values():
        #     setattr(node,'data',{})
        #print(self.nodes["Katowice"].data)
        #self.save_graph(self.nodes)
    def export_data(self):
        """Metoda wywoływana, gdy chcesz wysłać coś na zewnątrz"""
        results="test"
        
       
        if self.on_data_change:
            self.on_data_change(results)   
        
    

    # def ant_test(self,node):
    #     ant = Ant(node,1.0,1.0)
    #     print(f'wezel startowy {ant.current_node.name}')
    #     ant_next_node = ant.choose_next_node()
    #     print(f'nowy wezel  {ant_next_node.name}')
    #     ant_next_node = ant.choose_next_node()
    #     print(f'nowy wezel  {ant_next_node.name}')

    # def save_graph(self,nodes, filename="graph_data.pkl"):
    #     try:
    #         with open(filename, "wb") as f:  # "wb" zapis binarny
    #             pickle.dump(nodes, f)
    #         print(f"The graph has been saved to a file {filename}") 
    #     except Exception as e:
    #         print(f"Error while writing to a file: {e}")

    # def load_graph(self,filename="graph_data.pkl"):
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    
    #     # 2. Tworzymy ścieżkę "o gałąź wyżej" (parent directory)
    #     # abspath sprząta ewentualne kropki i ukośniki
    #     parent_dir = os.path.dirname(current_dir)
        
    #     # 3. Łączymy to z nazwą pliku
    #     full_path = os.path.join(parent_dir, filename)
    #     try:
    #         with open(filename, "rb") as f:  # "rb" odczyt binarny
    #             nodes = pickle.load(f)
    #         print(f"The graph has been loaded from a file {filename}") 
    #         return nodes
    #     except FileNotFoundError:
    #         print("Save file not found.")
    #         return {}

    def load_graph(self, filename="graph_data.pkl"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, 'data', filename)
        
        if os.path.exists(full_path):
            try:
                with open(full_path, "rb") as f:
                    nodes = pickle.load(f)
                #print(f"The graph has been loaded from a file")
                return nodes
            except Exception as e:
                #print(f"Error. {e}")
                return {}
        
    def create_node_buttons(self):
        def node_on_click(node, instance ):
            print(f'wezel {node.name}')
            pass

        for name, node in self.nodes.items():
            
            btnsize = (node.size ** 0.5) * 1.2
            btn = Button(
                size_hint=(None, None),
                size=(btnsize, btnsize),
                background_normal='',      
                background_color=(0,0,0,0) 
            )
            btn.bind(on_release=partial(node_on_click, node))
            node.data["button"]=btn
            self.add_widget(btn)
            

    

    def draw_graph(self, *args):
        
        def circle_collide(instance, x, y):
    
            center_x, center_y = instance.center
            radius = instance.width / 2
            distance = ((x - center_x)**2 + (y - center_y)**2)**0.5
            return distance <= radius

        self.canvas.clear()
        w, h = self.width, self.height

        with self.canvas:
            #Rysowanie tła 
            
            #Rectangle(source='data/mapa_polski.jpg', pos=(0, 0), size=self.size) #konturowa
            #Rectangle(source='data/mapa2.png', pos=(0, 0), size=self.size) #googlemaps
            #Color(1, 1, 1, 1) rgba: 0.6, 0.6, 0.6, 1
            Color(0.6, 0.6, 0.6, 1)
            Rectangle(pos=(0, 0), size=self.size)
            #Rectangle(source='data/mapa3.jpg', pos=(0, 0), size=self.size) #galaktyka
            Color(0, 0, 0, 1)
            for name,node in self.nodes.items():
                x1, y1 = node.pos_x, node.pos_y
                for neighbor in node.neighbors:
                    if name < neighbor.name:
                        x2, y2 = neighbor.pos_x, neighbor.pos_y
                        Line(points=[x1*w, y1*h, x2*w, y2*h], width=1)

            for name,node in self.nodes.items():
                x1, y1, size = node.pos_x * w, node.pos_y * h , node.size
                Color(1, 0.3, 0, 0.9) if size > 300 else Color(0, 0.6, 1, 0.8)
                size = (size ** 0.5) * 1.2
                btn = node.data["button"]
                btn.size=(size,size)
                btn.center = (x1,y1)
                btn.collide_point = MethodType(circle_collide, btn)
                
                    
                Ellipse(pos=(x1 - size/2, y1 - size/2), size=(size, size))
    
            for name,node in self.nodes.items():
                x1, y1 = node.pos_x * w, node.pos_y * h
                
                if name not in aglomeracja_slaska or name == 'Katowice':  
                    if name == 'Katowice':
                        name = "Katowice*"
                    city_label = CoreLabel(text=name, font_size=15)
                    city_label.refresh()
                    texture = city_label.texture
                    Color(0, 0, 0, 1)
                    Rectangle(
                        texture=texture, 
                        pos=(x1 - texture.size[0]/2, y1 - texture.size[1]/2), 
                        size=texture.size
                    )
                    
            
class AntColonyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def on_pre_enter(self):
        Clock.schedule_once(self.setup_graph)
        
       
        
        
        

        
    def on_enter(self, *args):
        
        self.simulationOn = False
        

    def setup_graph(self, dt):
        self.graph = GraphWidget()
        #self.graph.on_data_change = self.receive_stats
        
        
        if 'graphArea' in self.ids:
            self.ids.graphArea.clear_widgets()
            self.ids.graphArea.add_widget(self.graph)
    
    def start_stop(self,instance):
        if not self.simulationOn:
            print("on")
            #self.simulationOn = True
            #self.updateEvent = Clock.schedule_interval(self.update_points, 1/2 )
        else:
            print("off")
            #Clock.unschedule(self.updateEvent)
            #self.simulationOn = False


