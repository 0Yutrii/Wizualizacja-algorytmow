import numpy as np

class Ant:
    def __init__(self, start_node, alpha, beta):
        self.current_node = start_node
        self.visited_nodes = [start_node]
        self.alpha = alpha
        self.beta = beta
        self.total_distance = 0
        self.is_finished = False
    
    def choose_next_node(self):
        neighbors = self.current_node.neighbors
        unvisited = [n for n in neighbors.keys() if n not in self.visited_nodes]

        if not unvisited:
            self.is_finished = True
            return None
        
        next_node = np.random.choice(unvisited)
        
        #next_node = 

        distance = neighbors[next_node]
        self.total_distance += distance
        self.current_node = next_node
        self.visited_nodes.append(next_node)
        print(distance)
        return next_node
    
    def move(self):
        next_node = self.choose_next_node()
        pass
    
    def reset(self,start_node):
        pass
