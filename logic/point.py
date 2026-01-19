import numpy as np

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
        #print(self.position)
        
    
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


        