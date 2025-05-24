from settings import *

# pathfinding library
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder

class PathFinderBase():
    def __init__(self, board, positions):
        self.board = board
    
        self.stop_node = board[positions[1][0]][positions[1][1]]
        self.start_node = board[positions[0][0]][positions[0][1]]
        
        self.start_cords = positions[0]
        self.stop_cords = positions[1]
        
        board = [[0 if self.board[i][j].color == BRDR_COLOR else 1 for i in range(ROWS)] for j in range(COLS)]
        self.grid = Grid(matrix=board)
        self.start = self.grid.node(self.start_cords[0], self.start_cords[1])
        self.stop = self.grid.node(self.stop_cords[0], self.stop_cords[1])
        
        self.path = []
        self.open = []
        self.close = []
        self.i = 0
        self.j = 10
        
        self.runs = 0
    
    def convert(self, path):
        for i in range(ROWS):
            for j in range(COLS):
                node = self.grid.node(i,j)
                if node.closed:
                    self.board[i][j].color = CLOSED_COLOR
                    self.close.append(self.board[i][j])
                elif node.opened:
                    self.board[i][j].color = EDGE_COLOR
                    self.open.append(self.board[i][j])
        
        for node in path:
            self.path.append(self.board[node.x][node.y])
        
    def make_path(self, path):
        path[self.i].color = PATH_COLOR
        path[self.j].color = PATH_RUN_COLOR
        
        self.i = self.i + 1
        self.j = self.j + 1
        
        if self.i >= len(path):
            self.i = 0
        if self.j >= len(path):
            self.j = 0
            
        path[-1].color = START_COLOR
        path[0].color = STOP_COLOR

class AStar_pf(PathFinderBase):
    def __init__(self, board, positions):
        super().__init__(board, positions)
    
    def solve(self):
        if not self.path:
            finder = AStarFinder(diagonal_movement=True)
            path, self.runs = finder.find_path(self.start, self.stop, self.grid)
            
            self.convert(path)
            self.path.reverse()
        else:
            self.make_path(self.path)
        
        # CLOSE, OPEN, PATH
        return (len(self.close), len(self.open), len(self.path), self.runs)

class Dijkstra_pf(PathFinderBase):
    def __init__(self, board, positions):
        super().__init__(board, positions)
    
    def solve(self):
        if not self.path:
            finder = DijkstraFinder(diagonal_movement=True)
            path, self.runs = finder.find_path(self.start, self.stop, self.grid)
            
            self.convert(path)
            self.path.reverse()
        else:
            self.make_path(self.path)
            
        # CLOSE, OPEN, PATH
        return (len(self.close), len(self.open), len(self.path), self.runs)