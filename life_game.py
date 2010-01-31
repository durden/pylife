#!/opt/local/bin/python2.4

import Numeric
import sys
import time
import pygame
from pygame.locals import *


class Cell(object):
    """Individual cell"""
    def __init__(self):
        self.alive_curr_gen = False
        self.alive_next_gen = False
        self.generation_cnt = 0

class GameTable(object):
    """Game of life table"""
    def __init__(self, width, height, scale):
        self.screen = None
        self.scale_screen = None
        self.cells = []

        self.xscale = width/scale
        self.yscale = height/scale

        # 2-D array that cooresponds to pixels on surface
        self.px_arr = Numeric.zeros((self.xscale, self.yscale), 'i')

        # Create 2-D list of cells to coorespond to pixel array
        for xx in range(self.xscale):
            self.cells.append([])
            for yy in range(self.yscale):
                self.cells[xx].append(Cell())
        
        self.__init_graphics(width, height)
        self.__init_configuration()
        self.__prepare_generation()
        self.advance_generation()
        self.__drawfield()

    def __init_graphics(self, width, height):
        """Setup graphics (game board), etc."""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), 0, 8)
        self.scale_screen = pygame.surface.Surface((self.xscale, self.yscale),
                                                    0, 8)
        white = 255, 255, 255
        black = 0, 0, 0
        red = 255, 0, 0
        green = 0, 255, 0
        blue = 0, 0, 255

        self.screen.fill(black)
        self.scale_screen.fill(black)
        self.screen.set_palette([black, red, green, blue, white])
        self.scale_screen.set_palette([black, red, green, blue, white])

    def __init_configuration(self):
        """Setup initial alive cells"""
        for ii in range(20):
            self.cells[ii][50].alive_curr_gen = True

    def __drawfield(self):
        pygame.surfarray.blit_array(self.scale_screen, self.px_arr)
        temp = pygame.transform.scale(self.scale_screen,
                                        self.screen.get_size())
        self.screen.blit(temp, (0,0))
        pygame.display.update()
        return

    def __prepare_generation(self):
        """Apply rules of life to each cell"""
        for xx in range(self.xscale):
            for yy in range(self.yscale):
                cnt = self.__count_neighbors(xx, yy)
                if self.cells[xx][yy].alive_curr_gen:
                    if cnt < 2 or cnt > 3:
                        self.cells[xx][yy].alive_next_gen = False
                    else:
                        self.cells[xx][yy].alive_next_gen = True
                else:
                    if cnt == 3:
                        self.cells[xx][yy].alive_next_gen = True

                if self.cells[xx][yy].alive_next_gen:
                    self.cells[xx][yy].generation_cnt += 1
                else:
                    self.cells[xx][yy].generation_cnt = 0

    def __count_neighbors(self, x, y):
        """Count neighbors for given cell"""

        neighbors = 0
        left = x - 1
        right = x + 1
        up = y - 1
        down = y + 1

        # Check horizontal neighbors
        if left >= 0 and self.cells[left][y].alive_curr_gen:
            neighbors += 1
        if right < self.xscale and self.cells[right][y].alive_curr_gen:
            neighbors += 1

        # Check vertial neighbors
        if up >= 0 and self.cells[x][up].alive_curr_gen:
            neighbors += 1
        if down < self.yscale and self.cells[x][down].alive_curr_gen:
            neighbors += 1

        # Check top diagnoal neighbors
        if left >= 0 and up >= 0 and self.cells[left][up].alive_curr_gen:
            neighbors += 1
        if right < self.xscale and up < self.yscale and \
                self.cells[right][up].alive_curr_gen:
            neighbors += 1

        # Check bottom diagnoal neighbors
        if left >= 0 and down < self.yscale and \
                self.cells[left][down].alive_curr_gen:
            neighbors += 1
        if right < self.xscale and down < self.yscale and \
                self.cells[right][down].alive_curr_gen:
            neighbors += 1

        return neighbors

    def advance_generation(self):
        """Advance all cells by 1 generation""" 
        self.__prepare_generation()

        for xx in range(self.xscale):
            for yy in range(self.yscale):
                self.cells[xx][yy].alive_curr_gen = \
                    self.cells[xx][yy].alive_next_gen

                color = 0
                if self.cells[xx][yy].generation_cnt > 0:
                    if self.cells[xx][yy].generation_cnt >= 4:
                        color = 4
                    else:
                        color = self.cells[xx][yy].generation_cnt

                self.px_arr[xx][yy] = color

        self.__drawfield()

def setup():
    return GameTable(640,480, 4)

def run(table):
    while True:
        time.sleep(1)
        input(pygame.event.get())
        table.advance_generation()

def input(events): 
   for event in events: 
      if event.type == QUIT: 
         sys.exit(0) 
      else: 
         print event 

def tearDown():
    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    table = setup()
    run(table)
    tearDown()
