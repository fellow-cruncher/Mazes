from settings import *
import pygame

from base import Base

class BFS(Base):
    def __init__(self, board, positions):
        super().__init__(board)

        self.stop_node = board[positions[1][0]][positions[1][1]]
        self.start_node = board[positions[0][0]][positions[0][1]]
        self.start_node.g_cost = 0
        self.open.append(self.start_node)

        # BFS is just a Dijkstra with diagonal cost = 10 instead of 14.
        for direction in self.g_cost.keys():
            if len(direction) == 2:
                self.g_cost[direction] = 10
                
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
        return (len(self.close), len(self.open), len(self.path))
    
    def find_interested_nodes(self):
        nodes = []

        # BFS uses FIFO instead of [0] from sorted list.
        while self.open:
            node = self.open[0]
            self.open.remove(node)
            self.close.append(node)
            node.color = CLOSED_COLOR
            nodes.append(node)
            
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
                    checked_node.parent = node
                else:
                    continue