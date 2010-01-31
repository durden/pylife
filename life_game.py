#!/opt/local/bin/python2.4

import Numeric
import sys
import time
import pygame
from pygame.locals import *

white = 255,240,200
black = 20,20, 40
red = 255, 20, 40
green = 20,255,40
blue = 20,20,255

class Cell(object):
    """Individual cell"""
    def __init__(self):
        self.alive_curr_gen = False
        self.alive_next_gen = False
        self.generation_cnt = 0

class GameTable(object):
    """Game of life table"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cells = []

        SCALE = 4
        self.xscale = self.x/SCALE
        self.yscale = self.y/SCALE

        pygame.init()
        self.screen = pygame.display.set_mode((self.x, self.y), 0, 8)
        self.scale_screen = pygame.surface.Surface((self.xscale, self.yscale),
                                                    0, 8)

        self.screen.fill(black)
        self.scale_screen.fill(black)
        self.screen.set_palette( [black, red, green, blue, white] )
        self.scale_screen.set_palette( [black, red, green, blue, white] )

        self.px_arr = Numeric.zeros((self.xscale, self.yscale), 'i')

        # Create 2-D array of cells to coorespond to pixel array
        for xx in range(self.xscale):
            self.cells.append([])
            for yy in range(self.yscale):
                self.cells[xx].append(Cell())
        
        self.__init_configuration()
        self.__prepare_generation()
        self.advance_generation()
        self.__drawfield()

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

                if self.cells[xx][yy].alive_curr_gen:
                    if self.cells[xx][yy].generation_cnt == 1:
                        self.px_arr[xx][yy] = 2
                    elif self.cells[xx][yy].generation_cnt == 2:
                        self.px_arr[xx][yy] = 3
                    else:
                        self.px_arr[xx][yy] = 1
                else:
                    self.px_arr[xx][yy] = 0

        self.__drawfield()

def setup():
    return GameTable(640,480)

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
