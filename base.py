from settings import *
import pygame

class Base():
    def __init__(self, board, positions):

        self.board = board
        
        self.stop_node = board[positions[1][0]][positions[1][1]]
        self.start_node = board[positions[0][0]][positions[0][1]]
        
        self.close = []
        self.open = []
        self.path = []
        
        self.solve_time = 0
        self.start_time = pygame.time.get_ticks()
        
        self.i = 0
        self.j = 10

        self.direction = {
            'E': (1,0),
            'NE':(1,1),
            'N':(0,1),  
            'NW':(-1,1),
            'W':(-1,0),
            'SW':(-1,-1),
            'S':(0,-1),
            'SE':(1,-1),
        }
        
        self.g_cost = {
            'E':10,
            'NE':14,
            'N':10,
            'NW':14,
            'W':10,
            'SW':14,
            'S':10,
            'SE':14,
        }
    
    def make_path(self):
        current_node = self.stop_node
        
        while current_node != self.start_node:
            if current_node not in self.path:
                self.path.append(current_node)
            if current_node.parent != None:
                current_node = current_node.parent

        if current_node == self.start_node:
            if current_node not in self.path:
                self.path.append(self.start_node)
    
    def mark_path(self):
        self.path[self.i].color = PATH_COLOR
        self.path[self.j].color = PATH_RUN_COLOR
        
        self.i = self.i + 1
        self.j = self.j + 1
        
        if self.i >= len(self.path):
            self.i = 0
        if self.j >= len(self.path):
            self.j = 0

    def node_check(self, i, j):
        # Sprawdzamy czy koordynaty nie wykraczają poza GRID
        if i < 0 or j < 0 or i > ROWS-1 or j > COLS-1:
            return 0

        # Sprawdzamy czy NODE nie jest WALL
        if self.board[i][j].color == BRDR_COLOR:
            return 0
    
        # Sprawdzamy czy NODE nie jest w CLOSE
        if self.board[i][j] in self.close:
            return 0
        
        # Sprawdzamy czy NODE nie jest w OPEN
        if self.board[i][j] in self.open:
            return 0

        return 1