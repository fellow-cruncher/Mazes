import pygame
from math import inf
from settings import *

class Rectangle(pygame.sprite.Sprite):
    # performance
    __slots__ = ("image", "position", "rect", "g_cost", "h_cost", "f_cost", "parent", "color", "last_color")
    
    def __init__(self, position, offset, color, groups):
        super().__init__(groups)

        # setup
        self.image = pygame.Surface((10,10), pygame.SRCALPHA).convert()
        self.position = position
        self.rect = self.image.get_rect(topleft = (position[0]*10 + offset[0], position[1]*10 + offset[1]))
        
        # algorithm attributes
        self.g_cost = inf # Dijkstra, AStar
        self.h_cost = inf # AStar
        self.f_cost = inf # AStar
        self.parent = None # Dijkstra, AStar, DFS
        
        # colors
        self.color = color
        self.last_color = None
    
    def update(self):
        # performance
        if self.color != self.last_color:
            self.image.fill(self.color)
            self.last_color = self.color