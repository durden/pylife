#!/opt/local/bin/python2.4

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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cells = []

        pygame.init()          
        self.window = pygame.display.set_mode((self.x, self.y))
        self.px_arr = pygame.PixelArray(self.window)

        # Create 2-D array of cells to coorespond to pixel array
        for xx in range(self.x):
            self.cells.append([])
            for yy in range(self.y):
                self.cells[xx].append(Cell())
        
        self.__init_configuration()
        self.__prepare_generation()
        self.advance_generation()
        pygame.display.update()

    def __init_configuration(self):
        """Setup initial alive cells"""
        for ii in range(20):
            self.cells[ii][50].alive_curr_gen = True

    def __prepare_generation(self):
        """Apply rules of life to each cell"""
        for xx in range(self.x):
            for yy in range(self.y):
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
        if right < self.x and self.cells[right][y].alive_curr_gen:
            neighbors += 1

        # Check vertial neighbors
        if up >= 0 and self.cells[x][up].alive_curr_gen:
            neighbors += 1
        if down < self.y and self.cells[x][down].alive_curr_gen:
            neighbors += 1

        # Check top diagnoal neighbors
        if left >= 0 and up >= 0 and self.cells[left][up].alive_curr_gen:
            neighbors += 1
        if right < self.x and up < self.y and \
                self.cells[right][up].alive_curr_gen:
            neighbors += 1

        # Check bottom diagnoal neighbors
        if left >= 0 and down < self.y and \
                self.cells[left][down].alive_curr_gen:
            neighbors += 1
        if right < self.x and down < self.y and \
                self.cells[right][down].alive_curr_gen:
            neighbors += 1

        return neighbors

    def advance_generation(self):
        """Advance all cells by 1 generation""" 
        self.__prepare_generation()

        for xx in range(self.x):
            for yy in range(self.y):
                self.cells[xx][yy].alive_curr_gen = \
                    self.cells[xx][yy].alive_next_gen

                if self.cells[xx][yy].alive_curr_gen:
                    if self.cells[xx][yy].generation_cnt == 1:
                        self.px_arr[xx][yy] = 0xff0000
                    elif self.cells[xx][yy].generation_cnt == 2:
                        self.px_arr[xx][yy] = 0x00ff00
                    else:
                        self.px_arr[xx][yy] = 0x0000ff
                else:
                    self.px_arr[xx][yy] = 0x000000

        pygame.display.update()


def setup():
    return GameTable(200, 200)

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

#for ii in range(2):
#    arr[0:100] = 0xff0000
#    pygame.display.update()
#    time.sleep(1)
#    arr[0:100] = 0x00ff00
#    pygame.display.update()
#    time.sleep(1)

if __name__ == "__main__":
    table = setup()
    print "1"
    run(table)
    print "2"
    tearDown()
