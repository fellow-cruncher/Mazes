from settings import *
from random import choice
import pygame

from base import Base

class DFS(Base):
    def __init__(self, board, positions):
        super().__init__(board, positions)
        
        self.current_node = self.start_node

    def solve(self):
        if self.stop_node not in self.close:
            options = self.search_options(self.current_node)
            for node in options:
                node.parent = self.current_node
                
            self.decide(options)

            if self.stop_node.parent != None:
                self.make_path()
            
            self.solve_time = pygame.time.get_ticks() - self.start_time
        else:
            self.mark_path()

        self.start_node.color = START_COLOR
        self.stop_node.color = STOP_COLOR
        
        # (CLOSE, OPEN, PATH)
        #return (len(self.close), len(self.open), len(self.path))
        return (len(self.close), len(self.open), len(self.path) if len(self.path) != 0 else UNKNOWN, str((round(self.solve_time / 100) / 10))+"s")
    
    def decide(self, options):
            if options:
                random_node = choice(options)

            # Jeżeli NODE ma więcej, niż 1 opcji przejścia
            # To wybierz jedną, a resztę z nich dodaj do openu
            if len(options) > 1:
                self.current_node = random_node

                if self.current_node is not self.start_node:
                    self.current_node.color = CLOSED_COLOR
                self.close.append(self.current_node)
                options.remove(self.current_node)
                
                for node in options:
                    node.color = EDGE_COLOR
                    
                    # Lista OPEN w DFS to po prostu stack - LIFO. 
                    self.open.append(node)
                    
            # Jeżeli ma tylko jedną, idź tam
            elif options:
                self.current_node = random_node
                
                if self.current_node is not self.start_node:
                    self.current_node.color = CLOSED_COLOR
                self.close.append(self.current_node)

            # Jeżeli nie ma żadnej, wybierz jedną z góry stacka - LIFO
            else:
                self.current_node = self.open[-1]
                if self.current_node is not self.start_node:
                    self.current_node.color = CLOSED_COLOR
                    
                self.open.remove(self.current_node)
                self.close.append(self.current_node)
        
    def search_options(self, node):
        options = []

        # Dowiedzenie się jakie mamy opcje
        for direction in self.direction.keys():
            i = int((node.position[0] + self.direction[direction][0]))
            j = int((node.position[1] + self.direction[direction][1]))
            
            if self.node_check(i,j):
                options.append(self.board[i][j])
            else:
                continue
        
        return options