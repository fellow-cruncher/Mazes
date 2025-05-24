import pygame
from random import randint, shuffle, randrange, random
from rectangle import Rectangle
from settings import *

class Maze:
    def __init__(self, groups):
        self.all_sprites = groups
        self.window = pygame.display.get_surface()
    
    def create(self, flag="full"):
        if flag == "empty":
            color_board = self.create_empty()
        elif flag == "full":
            color_board = self.create_full()
        else:
            raise Exception("Wrong flag value")

        return (color_board, self.mark(color_board))

    def create_full(self):
        color_board = [[BRDR_COLOR for _ in range(COLS)] for _ in range(ROWS)]
        
        # Wybierz losowy punkt startowy z nieparzystymi współrzędnymi
        start_y = randrange(0, ROWS, 2)
        start_x = randrange(0, COLS, 2)
        stack = [(start_y, start_x)]
        color_board[start_y][start_x] = BRD_COLOR

        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # góra, dół, lewo, prawo

        while stack:
            current_y, current_x = stack[-1]
            shuffle(directions)
            found = False

            for dy, dx in directions:
                new_y = current_y + dy
                new_x = current_x + dx

                if 0 <= new_y < ROWS and 0 <= new_x < COLS:
                    if color_board[new_y][new_x] == BRDR_COLOR:
                        # Usuń ścianę między obecną a nową komórką
                        wall_y = current_y + dy // 2
                        wall_x = current_x + dx // 2
                        color_board[wall_y][wall_x] = BRD_COLOR
                        color_board[new_y][new_x] = BRD_COLOR
                        stack.append((new_y, new_x))
                        found = True
                        break
            
            if not found:
                stack.pop()
        
        return color_board

    def set_level(self, color_board, percent):
        new_board = [row[:] for row in color_board]

        for i in range(0, ROWS):
            for j in range(0, COLS):
                if i%2 == 0 or j%2 == 0:
                    if random() > float(percent / 100):
                        if new_board[i][j] == BRDR_COLOR:
                            new_board[i][j] = BRD_COLOR
        
        return new_board

    def create_empty(self):
        color_board = [[BRD_COLOR for _ in range(COLS)] for _ in range(ROWS)]
        
        return color_board

    def mark(self, color_board):
        positions = []

        while True:
            i = randint(0,int(ROWS*0.2))
            j = randint(0,int(COLS*0.2))
            
            if color_board[i][j] == BRD_COLOR:
                color_board[i][j] = START_COLOR
                positions.append((i,j))
                break
    
        while True:
            i = randint(int(ROWS*0.8),ROWS-1)
            j = randint(int(COLS*0.8),COLS-1)
            
            if color_board[i][j] == BRD_COLOR:
                color_board[i][j] = STOP_COLOR
                positions.append((i,j))
                break

        return positions
    
    def draw(self, board, index):
        return_board = []
        for i in range(ROWS):
            sub_list = []
            for j in range(COLS):
                sub_list.append(Rectangle((i,j), BRD_POS[index], board[i][j], self.all_sprites))
            
            return_board.append(sub_list)
        
        return return_board
    
    def set_mazes(self, color_board, openness):
        # Sortuj pary (indeks, wartość) malejąco po wartości
        sorted_pairs = sorted(enumerate(openness), key=lambda x: -x[1])
        
        # Inicjalizuj wszystkie boards jako None
        boards = [None] * len(openness)
        
        # Stwórz kopię początkowego color_board jako bazę
        current_board = [row[:] for row in color_board]
        
        # Przetwarzaj w kolejności od największej wartości
        for i, (index, value) in enumerate(sorted_pairs):
            if i == 0:
                # Pierwszy element: użyj rzeczywistej wartości (np. 90 zamiast 100)
                procent = value
            else:
                # Oblicz procent względem poprzedniej wartości
                prev_value = sorted_pairs[i-1][1]
                procent = (value / prev_value) * 100.0 if prev_value > 0 else 0
            
            # Generuj nowy labirynt na podstawie aktualnego current_board
            new_board = self.set_level(current_board, procent)
            boards[index] = self.draw(new_board, index)
            
            # Zaktualizuj current_board do nowo wygenerowanego labiryntu
            current_board = new_board
        
        return boards