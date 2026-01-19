import numpy as np

class Ant:
    def __init__(self, start_node, alpha, beta,all_nodes_count=30):
        self.current_node = start_node
        self.visited_nodes = [start_node]
        self.alpha = alpha
        self.beta = beta
        self.total_distance = 0
        self.is_finished = False
        self.failed=False
        self.all_nodes_count=all_nodes_count
    
    def choose_next_node(self):
        if len(self.visited_nodes) == self.all_nodes_count:
            self.is_finished = True
            return None
        neighbors = self.current_node.neighbors
        unvisited = [n for n in neighbors.keys() if n not in self.visited_nodes]

        if not unvisited:
            self.is_finished = True
            self.failed = True
            return None
        
        #return np.random.choice(unvisited)
        probabilities = []
        total_attractiveness = 0.0
        #print("   -------------------")
        for candidate in unvisited:
            tau=self.current_node.pheromones[candidate]
            distance = neighbors[candidate]
            eta = 1.0/distance

            attractiveness = (tau**self.alpha) * (eta**self.beta)
            probabilities.append((candidate,attractiveness))
            #print(f'{candidate.name} atr={attractiveness}')
            total_attractiveness += attractiveness

        if total_attractiveness==0:
            print("total_attractiveness=0 ")
            return np.random.choice(unvisited)
        
        pick = np.random.uniform(0,total_attractiveness)
        current_sum = 0
        for candidate, score in probabilities:
            current_sum += score
            if current_sum >= pick:
                return candidate 
            
       
        
        
        
    def move(self):
        next_node = self.choose_next_node()

        if next_node is None:
            return
        
        distance = self.current_node.neighbors[next_node]
        self.total_distance += distance
        #print(f'{self.current_node.name}->{next_node.name}~{distance}')
        self.current_node = next_node
        self.visited_nodes.append(next_node)
    
    def reset(self,start_node):
        pass
