from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
from kivy.config import Config
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt


import settings.klasa1 as klasa1
from settings.pso_settings import PsoSettingsMenu


#Config.set('input', 'mouse', 'mouse,disable_on_activity')
#Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# class CustomDropDown(BoxLayout):
#     expanded = False

#     def toggle(self):
#         self.expanded = not self.expanded
#         self.ids.extra_text.height = 60 if self.expanded else 0
#         self.ids.extra_text.opacity = 1 if self.expanded else 0

#     pass

class Point:
    w = 0.7
    c1 = 1.49
    c2 = 1.49
    v_max = 0.1
    
    def __init__(self, range,get_z,globalBest):
        
        self.position=np.array([.0, .0, .0]) 
        self.position[0] = np.random.uniform(low=range[0],high=range[1])
        self.position[1] = np.random.uniform(low=range[2],high=range[3])
        self.position[2] = (get_z(self.position[0],self.position[1]))
        self.velocity  =np.random.rand(2) - 0.5
        self.personalBest = self.position
        self.globalBest = globalBest
        print(self.position)
        
    
    def show_pos(self):
        print(self.position[0], self.position[1], self.velocity,self.PB)

    def move(self,get_z):
        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]
        self.position[2] = get_z(self.position[0],self.position[1])

    def update_velocity(self):
        for i in range(len(self.velocity)):
            self.velocity[i] = np.clip(
                ( self.w*self.velocity[i] + self.c1 * np.random.rand() * (self.personalBest[i]-self.position[i]) 
                + self.c2 * np.random.rand() * (self.globalBest[i]-self.position[i])
                ),-self.v_max, self.v_max)


        

class WizualizacjaAlgorytmow(Screen):
    plot_range = [-6,6,-6,6]
    swarm_size = 25
    math_fun = 1
    plot_density = 0.1

    
    
    data_labels_names = {
        "globalBest": "Global best value ",
        "globalBestCords": "Global best coords ",
        "pointPersonalBest": "Personal best value ",
        "personalBestCords": "Personal best coords ",
        "pointPosValue": "Point's value ",
        "pointPos": "Point's coords ",
        "pointVelocity": "Point's velocity "
    }

    # data_labels_mapping = {
    #         "globalBest": point.globalBest[2],
    #         "globalBestCords": (point.globalBest[0], point.globalBest[1]),
    #         "personalBestCords": (point.personalBest[0],point.personalBest[1]),
    #         "pointPersonalBest": point.personalBest[2],
    #         "pointPosValue": point.position[2],
    #         "pointPos": (point.position[0],point.position[1]),
    #         "pointVelocity": (point.velocity[0],point.velocity[1])
    #     }

    def on_pre_enter(self):
        
        self.updateEvent = None
        self.plotPoints = None
        self.selected_point=None
        self.get_z = None
        self.fig = plt.figure()
        self.fig.patch.set_facecolor((0, 0, 0, 0))
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.set_facecolor((0, 0, 0, 0))
        self.plot=FigureCanvasKivyAgg(self.fig)
        self.drop_down_menu()
        
        
        
        

        
    def on_enter(self, *args):
        if self.updateEvent is not None:
            Clock.unschedule(self.updateEvent)
        self.simulationOn = False
        self.ids.graphArea.clear_widgets()
        self.ids.graphArea.add_widget(self.plot)
        self.ax.clear()
        self.set_fun(self.math_fun)
        X = np.arange(self.plot_range[0], self.plot_range[1], self.plot_density)
        Y = np.arange(self.plot_range[2], self.plot_range[3], self.plot_density)
        X, Y = np.meshgrid(X, Y)
        Z = self.get_z(X,Y)
        self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)
        #self.ax.plot_surface(X, Y, Z, cmap='ocean', alpha=0.6)
        
        self.create()
        self.ax.figure.canvas.draw_idle()

        self.clear_data()

    def update_points(self,dt):
        
        for p in self.points:
            p.update_velocity()
            p.move(self.get_z)
            p.personalBest=self.get_best(p.personalBest,p.position)
            #print(p.personalBest[2])

        self.check_global_best()
        self.X=[p.position[0] for p in self.points]
        self.Y=[p.position[1] for p in self.points]
        self.Z=[p.position[2] for p in self.points]

        if self.selected_point is not None:
            self.set_data(self.selected_point)
        self.plotPoints._offsets3d = (self.X, self.Y, self.Z)
        self.ax.figure.canvas.draw_idle()
        
    def change_point_color(self, previous_point, new_point):
        
        all_colors = np.zeros((self.swarm_size, 4))
        all_colors[:] = [1, 0, 0, 1]  

        all_colors[new_point] = [0, 0, 0, 1] 

        self.plotPoints.set_facecolors(all_colors)
        self.plotPoints.set_edgecolors(all_colors)
        
        print(all_colors) 
        
        self.ax.figure.canvas.draw_idle()


        pass
        
    def set_fun(self,op):
        functions_dict={ 1 :self.get_z1,
                         2 :self.get_z2,
                         3 :self.get_z3,
                         4 :self.get_z4}
        self.get_z=functions_dict[op]

    def get_z1(self,X,Y): #Himmelblau’s function

        return np.sqrt(np.power((np.power(X,2)+Y-11),2) + np.power((np.power(Y,2)+X-7),2))
    
    def get_z2(self,X,Y):
        return np.power((1-X),2)+100*np.power((Y-np.power(X,2)),2)

        '''
        (a - x)^2 + b*(y - x^2)^2
        '''
    def get_z3(self, X, Y):
        A=10
        return 2*A + (X**2 - A * np.cos(2*np.pi*X)) + (Y**2 - A * np.cos(2*np.pi*Y))
    
    def get_z4(self, X, Y):
        term1 = -20.0 * np.exp(-0.2 * np.sqrt(0.5*(X**2 + Y**2)))
        term2 = -np.exp(0.5*(np.cos(2*np.pi*X) + np.cos(2*np.pi*Y)))
        return term1 + term2 + np.e + 20

    def check_global_best(self):
        best=np.array([0,0,float('inf')])
        for point in self.points:
            best=self.get_best(best,point.personalBest)
        self.globalBest[:]=best
        #print(f'global best {self.globalBest[2]}')

    def get_best(self,current,new):
        if(len(current)==0 or current[2]>new[2]):
            return [new[0],new[1],new[2]]
        else:
            return [current[0],current[1],current[2]]

    def create(self):
        self.globalBest = np.array([0,0,float('inf')])
        self.points = None
        self.points = [Point(self.plot_range,self.get_z,self.globalBest) for _ in range(self.swarm_size)]
        
        self.X=[p.position[0] for p in self.points]
        self.Y=[p.position[1] for p in self.points]
        self.Z=[p.position[2] for p in self.points]
        
        self.check_global_best()
        #print(self.globalBest[2])
        #print(Point.c1)
        self.plotPoints = self.ax.scatter(self.X, self.Y, self.Z, color='red', alpha=1)

##########################################################################################
    

        
            
    def start_stop(self,instance):
        if not self.simulationOn:
            #print("on")
            self.simulationOn = True
            self.updateEvent = Clock.schedule_interval(self.update_points, 1/2 )
        else:
            #print("off")
            Clock.unschedule(self.updateEvent)
            self.simulationOn = False

    def rotate_left(self,instance):
        elev, azim = self.ax.elev, self.ax.azim
        self.ax.view_init(elev, azim - 10)
        self.ax.figure.canvas.draw_idle()

    def rotate_right(self,instance):
        elev, azim = self.ax.elev, self.ax.azim
        self.ax.view_init(elev, azim + 10)
        self.ax.figure.canvas.draw_idle()

    def rotate_up(self,instance):
        elev, azim = self.ax.elev, self.ax.azim
        self.ax.view_init(elev + 10, azim)
        self.ax.figure.canvas.draw_idle()

    def rotate_down(self,instance):
        elev, azim = self.ax.elev, self.ax.azim
        self.ax.view_init(elev - 10, azim)
        self.ax.figure.canvas.draw_idle()

    def open_options(self,instance):
        plot_data = [
            self.plot_range,
            self.swarm_size,
            self.math_fun,
            self.plot_density
            ]
        popup = PsoSettingsMenu(data=plot_data,point=Point,callback_apply=self.apply_settings)
        popup.open()

    def apply_settings(self, temp_plot_range,temp_swarm_size,temp_math_fun):
        
        self.plot_range = temp_plot_range
        self.swarm_size = temp_swarm_size
        self.math_fun = temp_math_fun
        
        #self.on_enter(self)
    
    def set_point(self,instance,point_index):
        self.change_point_color(self.selected_point,point_index)
        self.selected_point=point_index
        self.ids.mainButton.text = f'Point {point_index + 1}'
        self.set_data(point_index)

    def set_data(self,selected_point):
        point=self.points[selected_point]
        
        data_labels_mapping = {
            "globalBest": point.globalBest[2],
            "globalBestCords": (point.globalBest[0], point.globalBest[1]),
            "pointPersonalBest": point.personalBest[2],
            "personalBestCords": (point.personalBest[0],point.personalBest[1]),
            "pointPosValue": point.position[2],
            "pointPos": (point.position[0],point.position[1]),
            "pointVelocity": (point.velocity[0],point.velocity[1])
        }


        for widget_id, value in data_labels_mapping.items():
            formatted_value = f''

            display_name = self.data_labels_names.get(widget_id,widget_id)

            
            if isinstance(value,tuple):
                for value_index in range(len(value)):
                    formatted_value = formatted_value + f"{value[value_index]:.4f} "
            else:
                formatted_value=f"{value:.4f}"
            self.ids[widget_id].text = f'[color=ff0000][b]{display_name}[/b][/color]\n{formatted_value}'

        #self.ids.globalBest.text ='[b][color=000000]'+ f'{self.points[point_index].globalBest[2]}' +'[/color][/b]'
    def clear_data(self):
        for widget_id, value in self.data_labels_names.items():
            self.ids[widget_id].text = f''
    

    def drop_down_menu(self):

        # self.mainbutton = Button(
        #     text='select point',
        #     size_hint=(None, None),
        #     size=(150, 50)
        # )

        # anchor = AnchorLayout(
        #     anchor_x='center',
        #     anchor_y='center',
        #     size_hint_y=None,
        #     height=60
        # )
        # anchor.add_widget(self.mainbutton)
        # self.ids.data.add_widget(anchor)

        def open_dropdown(instance):
            dropdown = DropDown()

            for point in range(self.swarm_size):
                btn = Button(
                    text=f'Point {point + 1}',
                    size_hint_y=None,
                    height=44
                )
                btn.bind(on_release=lambda inst,idx=point: dropdown.select(idx))
                dropdown.add_widget(btn)

            dropdown.bind(
                on_select=self.set_point
            )

            dropdown.bind(
                on_dismiss=lambda *_: dropdown.clear_widgets()
            )

            dropdown.open(instance)

        self.ids.mainButton.bind(on_release=open_dropdown)

        

        
        


    

        




'''



np.pow((np.pow(X,2)+Y-11),2) + np.pow((np.pow(Y,2)+X-7),2)

(x^2 + y - 11)^2 + (x + y^2 - 7)^2
+ np.pow((np.pow(Y,2)+X-7),2) Z = np.sin(R)

z'= 4x^3 +4xy - 42 * x +2*y^2-14
4  *np.pow(x,3) + 4 * x * y - 42 * np.pow(y,2) - 14



canvas:
                Color:
                    rgba: 0.2, 0.2, 0.2, 1 
                Rectangle:
                    pos: self.pos
                    size: self.size
'''
