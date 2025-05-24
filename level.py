import pygame
from settings import *
from maze import Maze
#from info import Info

from dfs import DFS
from dijkstra import Dijkstra
from astar import AStar

from gridsearch import GridSearch as GS
from info import Text_40

class Level:
    def __init__(self):
        # surfaces
        self.window = pygame.display.get_surface()
        self.maze_background = pygame.Surface(BRDR_SIZE)
        self.maze_background.fill(BRDR_COLOR)
        
        # infosy
        self.infosy = pygame.image.load('infos.png').convert()
        self.infosy_rect = self.infosy.get_rect(topleft = (0,461))
        
        # groups
        self.all_sprites = pygame.sprite.Group()
        
        # maze
        self.maze = Maze(self.all_sprites)

        # solvers
        self.boards = []
        self.set_index = -1
        
        self.font_40 = pygame.font.Font('fonts/font_40.otf', 40)
        self.font_60 = pygame.font.Font('fonts/font_60.ttf', 60)

        self.stats = [[None for _ in range(4)] for _ in range(6)]
        self.levels = [None for _ in range(6)]

        # state
        self.active = False
        
        # results
        # CLOSE, OPEN, PATH, TIME
        self.results = [None for _ in range(4)]

        # setup
        self.init_setup()
        
    def init_setup(self):
        self.window.fill(BACKGROUND_COLOR)
        
        for i in range(len(self.stats)):
            for j in range(4):
                self.stats[i][j] = Text_40(UNKNOWN, CRIT_POS[i][j], NUM_COLOR, self.font_40)

            self.levels[i] = Text_40(UNKNOWN, (LEVEL_POS[i]), LEV_COLOR, self.font_40)

            if i < 4:
                pygame.draw.line(self.window, LINE_COLOR, LINES_STARTS[i], LINES_ENDS[i], 20)

            self.window.blit(self.maze_background, BRDR_POS[i])
            
    def refresh(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_SPACE]:
            self.all_sprites.empty() 
            self.boards.clear()
            
            self.color_board, self.positions = self.maze.create()
            self.set_index += 1
            current_set = SETS[self.set_index % len(SETS)]
            
            for i in range(len(self.stats)):
                self.levels[i].text = f"{(current_set[i])}"
            self.boards = [row[:] for row in self.maze.set_mazes(self.color_board, current_set)]

            self.solvers = [AStar(self.boards[0], self.positions), DFS(self.boards[1], self.positions), Dijkstra(self.boards[2], self.positions),
                            GS("AStar", self.boards[3]),           GS("DFS", self.boards[4]),           GS("Dijkstra", self.boards[5])]
            
            self.active = True

    def run(self):
        self.refresh()
        self.window.blit(self.infosy, self.infosy_rect)

        # Making stats visible
        for i in range(len(self.stats)):
            for j in range(4):
                self.all_sprites.add(self.stats[i][j])
            self.all_sprites.add(self.levels[i])
        
        # solving
        if self.active:
            for i in range(len(self.solvers)):
                if self.solvers[i]:
                    self.stats[i][0].text, self.stats[i][1].text, self.stats[i][2].text, self.stats[i][3].text = self.solvers[i].solve()

        self.all_sprites.update()
        self.all_sprites.draw(self.window)