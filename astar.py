from settings import *
import pygame

from base import Base

class AStar(Base):
    def __init__(self, board, positions):
        super().__init__(board, positions)
        
        self.start_node.g_cost = 0
        self.start_node.h_cost = self.calculate_h_cost(self.stop_node)
        self.start_node.f_cost = self.start_node.g_cost + self.start_node.h_cost
        self.open.append(self.start_node)
    
    def calculate_h_cost(self, node):
        dx = abs(node.position[0] - self.stop_node.position[0])
        dy = abs(node.position[1] - self.stop_node.position[1])
        
        d1 = 10
        d2 = 14
        
        return d1*(dx+dy) + (d2 - 2 * d1) * min(dx, dy)

    def solve(self):
        if self.open and self.stop_node not in self.close:    
            interested_nodes = self.find_interested_nodes()
            self.affect_neighbours(interested_nodes)
            
            if self.stop_node.parent is not None:
                self.make_path()

            self.solve_time = pygame.time.get_ticks() - self.start_time
        else:
            self.mark_path()
        
        self.start_node.color = START_COLOR
        self.stop_node.color = STOP_COLOR
        
        # CLOSE, OPEN, PATH
        return (len(self.close), len(self.open), len(self.path) if len(self.path) != 0 else UNKNOWN, str((round(self.solve_time / 100) / 10))+"s")
    
    def find_interested_nodes(self):
        nodes = []
        
        # Stortujemy w ten sposób, aby [0] był NODE z najmniejszym COST
        # Usuwamy z OPEN, dodajemy do CLOSE
        node = sorted(self.open, key=lambda x: x.f_cost)[0]
        
        self.open.remove(node)
        self.close.append(node)
        node.color = CLOSED_COLOR
        nodes.append(node)

        #while self.open:
        #    next_node = sorted(self.open, key=lambda x: x.f_cost)[0]
        #    if next_node.f_cost != node.f_cost:
        #        break
        #    else:
        #        self.open.remove(next_node)
        #        self.close.append(next_node)
        #        next_node.color = CLOSED_COLOR
        #        nodes.append(next_node)
            
        return nodes
    
    def affect_neighbours(self, interested_nodes):

        # Dla każdego NODE z OPEN szukamy NODE'ów w każdym kierunku
        for node in interested_nodes:
            for direction in self.direction.keys():
                # Ustalamy koordynaty NODE, który będzie sprawdzany
                i = int((node.position[0] + self.direction[direction][0]))
                j = int((node.position[1] + self.direction[direction][1]))
                
                # Sprawdzamy czy wybrany NODE jest ok
                if self.node_check(i, j):
                    checked_node = self.board[i][j]

                    # Dodajemy do OPEN, ustalamy COST i PARENT
                    self.open.append(checked_node)
                    checked_node.color = EDGE_COLOR
                    checked_node.g_cost = node.g_cost + self.g_cost[direction]
                    checked_node.h_cost = self.calculate_h_cost(checked_node)
                    checked_node.f_cost = checked_node.g_cost + checked_node.h_cost
                    checked_node.parent = node
                else:
                    continue