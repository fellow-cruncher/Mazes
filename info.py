import pygame
from settings import *

class Text_60(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, font_60, groups):
        super().__init__(groups)
        
        self.clock = pygame.time.Clock()

        self.image = font_60.render(text, False, color)
        self.rect = self.image.get_rect(midright = pos)

class Text_40(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, font_40):
        super().__init__()
        
        self.text = text
        self.last_text = None
        self.color = color
        self.pos = pos
        self.clock = pygame.time.Clock()
        
        self.font_40 = font_40

        self.image = self.font_40.render(str(self.text), False, self.color)
        self.rect = self.image.get_rect(midright = self.pos)
        
    def update(self):
        if self.last_text != self.text:
            self.image = self.font_40.render(str(self.text), False, self.color)
            self.rect = self.image.get_rect(midright = self.pos)
            
            self.last_text = self.text

#class Info():
#    def __init__(self, font_40, font_60, all_sprites):
#        self.font_40 = font_40
#        self.font_60 = font_60
#        self.all_sprites = all_sprites
#        
#        self.infos = []
#
#    def display_captions(self):
#        for i in range(len(NAMES)):
#            self.infos.append(Text_60(NAMES[i], 
#                              NAMES_POS[i],
#                              NAMES_COLOR,
#                              self.font_60,
#                              self.all_sprites))
#        
#        for i in [0,1,2]:
#            # CLOSE
#            for j in [0,1]:
#                self.infos.append(Text_40(CRITS[0], (CRIT_X[i], CRIT_Y[j]), CLOSED_COLOR, self.font_40))
#            # OPEN
#            for j in [2,3]:
#                self.infos.append(Text_40(CRITS[1], (CRIT_X[i],CRIT_Y[j]), EDGE_COLOR, self.font_40))
#
#        for i in [3,4,5]:
#            # TIME
#            for j in [0,1]:
#                self.infos.append(Text_40(CRITS[2], (CRIT_X[i]-15,CRIT_Y[j]), PLACE_COLOR, self.font_40))
#            # PATH
#            for j in [2,3]:
#                self.infos.append(Text_40(CRITS[3], (CRIT_X[i]-15, CRIT_Y[j]), PATH_COLOR, self.font_40))
    