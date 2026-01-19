import numpy as np
from ant import Ant

class AntManager:
    def __init__(self, graph_nodes, ant_count=20, alpha=1.0, beta=2.0, rho=0.1, start_node='Szczecin'):
        self.nodes = graph_nodes        
        self.ant_count = ant_count      
        self.alpha = alpha              # Waga feromonu
        self.beta = beta                # Waga odległości
        self.rho = rho                  # Współczynnik parowania
        self.ants = []
        self.start_node=start_node

        self.create_pheromones()
        self.reset_ants(self.start_node)

    def create_pheromones(self):
        for name,node in self.nodes.items():
            node.pheromones = {neighbor: 0.1 for neighbor in node.neighbors}
    
    def reset_ants(self,start_node):
        self.ants = [Ant(start_node, self.alpha, self.beta) for _ in range(self.ant_count)]

    def update(self):
        for ant in self.ants:
            ant.move()

        if all(ant.is_finished for ant in self.ants):
            self.apply_pheromone_update()

    def apply_pheromone_update(self):
        for node in self.nodes.values():
            for neighbor in node.pheromones:
                node.pheromones[neighbor] *= (1-self.rho)

        for ant in self.ants:
            pheromones = 100/ant.total_distance
            for i in range(len(ant.visited_nodes)-1):
                u, v = ant.visited_nodes[i],ant.visited_nodes[i+1]
                u.pheromones[v] += pheromones
                v.pheromones[u] += pheromones