import pygame, ctypes
from sys import exit
from level import Level
from settings import *

class Program:
    def __init__(self):
        pygame.init()
        ctypes.windll.user32.SetProcessDPIAware()
        self.window = pygame.display.set_mode((1920,1200), pygame.DOUBLEBUF)
        pygame.display.set_caption("A* vs. DFS vs. Dijkstra")
        self.clock = pygame.time.Clock()
        
        # level
        self.level = Level()
    
    def run(self):
        while(1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.level.run()
            
            #print(self.clock.get_fps())
            
            pygame.display.update()
            self.clock.tick(FPS)
                
if __name__ == '__main__':
    program = Program()
    program.run()