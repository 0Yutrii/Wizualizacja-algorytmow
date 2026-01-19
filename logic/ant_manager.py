import numpy as np
from logic.ant import Ant

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
        self.reset_ants(self.nodes[self.start_node])
        

    def create_pheromones(self):
        for name,node in self.nodes.items():
            node.pheromones = {neighbor: 0.1 for neighbor in node.neighbors}
    
    def reset_ants(self,start_node):
        self.ants = [
            Ant(start_node, self.alpha, self.beta, all_nodes_count=len(self.nodes))
            for _ in range(self.ant_count)
        ]

    def run(self, iterations=100):
        for _ in range(iterations):
            self.reset_ants(self.nodes[self.start_node])
            self.run_ants()
            self.apply_pheromone_update()
            if _ % 10 == 0:
                self.make_report()
        for ant_id, ant in enumerate(self.ants):
            if ant.is_finished == True:
                self.make_report(ant_id)

    def run_ants(self):
        for ant in self.ants:
            while not ant.is_finished:
                ant.move()
            

    def update(self):
        self.run_ants()
        self.apply_pheromone_update()

    def apply_pheromone_update(self):
        for node in self.nodes.values():
            for neighbor in node.pheromones:
                node.pheromones[neighbor] *= (1-self.rho)

        successful_ants = [ant for ant in self.ants if not ant.failed]
        for ant in successful_ants:
            pheromones = 100/ant.total_distance
            for i in range(len(ant.visited_nodes)-1):
                u, v = ant.visited_nodes[i],ant.visited_nodes[i+1]
                u.pheromones[v] += pheromones
                v.pheromones[u] += pheromones
    
    def make_report(self,ant_id=0):
        single_ant = self.ants[ant_id]
        
        total_distance = single_ant.total_distance
        road = [node.name for node in single_ant.visited_nodes]
        road_count = len(single_ant.visited_nodes)
        print(f'laczny dystans mrowki {ant_id} wyniosl {total_distance}. Trasa liczyla {road_count}')
        if road_count==50:
            print(f' i była {road}')