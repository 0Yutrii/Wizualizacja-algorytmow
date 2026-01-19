class Node:
    def __init__(self,name, pos_x, pos_y, size=300):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.neighbors = {}
        self.pheromones = {}
        self.data = {}

    def add_neighbor(self, neighbor_node, lenght):
        self.neighbors[neighbor_node]=lenght
    
    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            del self.neighbors[neighbor]
        del self

    def remove_node(self):
        for neighbor in self.neighbors.keys():
            neighbor.remove_neighbor(self)
        self.neighbors.clear()