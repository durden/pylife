#!/opt/local/bin/python2.4

"""
Small driver program to simulate a game of Conway's life.
"""

import sys
import time
import Numeric
import pygame
from pygame.locals import QUIT


class Cell(object):
    """Individual cell"""

    def __init__(self):
        self.alive_curr_gen = False
        self.alive_next_gen = False
        self.generation_cnt = 0


class GameTable(object):
    """Game of life table"""

    def __init__(self, width, height, scale, seed_file=None):
        self.screen = None
        self.scale_screen = None
        self.cells = []

        self.xscale = width / scale
        self.yscale = height / scale

        # 2-D array that cooresponds to pixels on surface
        self.px_arr = Numeric.zeros((self.xscale, self.yscale), 'i')

        # Create 2-D list of cells to coorespond to pixel array
        for xx in range(self.xscale):
            self.cells.append([])
            for yy in range(self.yscale):
                self.cells[xx].append(Cell())

        self._init_graphics(width, height)
        self._init_configuration(seed_file)
        self._center_on_alive_cells()
        self._prepare_generation()
        self.advance_generation()
        self._drawfield()

    def _init_graphics(self, width, height):
        """Setup graphics (game board), etc."""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), 0, 8)
        self.scale_screen = pygame.surface.Surface((self.xscale, self.yscale),
                                                    0, 8)
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)

        self.screen.fill(black)
        self.scale_screen.fill(black)
        self.screen.set_palette([black, red, green, blue, white])
        self.scale_screen.set_palette([black, red, green, blue, white])

    def _init_configuration(self, seed_file):
        """Setup initial alive cells"""

        if seed_file == None:
            return self._default_configuration()

        return self._parse_configuration_file(seed_file)

    def _default_configuration(self):
        """Setup hard-coded default alive cells"""
        for ii in range(20):
            self.cells[ii][50].alive_curr_gen = True

    def _parse_configuration_file(self, seed_file):
        """Parse given configuration file for starting generation"""
        try:
            file_obj = open(seed_file, 'r')
        except IOError:
            print "Unable to open file '%s', defaulting seed " % (seed_file)
            return self._default_configuration()

        xx = 0
        yy = 0

        for line in file_obj:
            # Signals 'comment' line to be skipped
            if line[0] != "!":
                for char in line:
                    if char == "O":
                        self.cells[xx][yy].alive_curr_gen = True
                    xx = xx + 1
                    if xx > self.xscale:
                        raise IOError("File width (%d) too wide for game" \
                                        "table width (%d)" % (xx, self.xscale))
                xx = 0
                yy = yy + 1
                if yy > self.yscale:
                    raise IOError("File height (%d) too large for game " \
                                    "table height (%d)" % (yy, self.yscale))

    def _drawfield(self):
        """Draw board"""
        pygame.surfarray.blit_array(self.scale_screen, self.px_arr)
        temp = pygame.transform.scale(self.scale_screen,
                                        self.screen.get_size())
        self.screen.blit(temp, (0, 0))
        pygame.display.update()

    def _prepare_generation(self):
        """Apply rules of life to each cell"""
        for xx in range(self.xscale):
            for yy in range(self.yscale):
                cnt = self._count_neighbors(xx, yy)
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

    def _count_neighbors(self, xx, yy):
        """Count neighbors for given cell"""

        neighbors = 0
        left = xx - 1
        right = xx + 1
        up = yy - 1
        down = yy + 1

        # Check horizontal neighbors
        if left >= 0 and self.cells[left][yy].alive_curr_gen:
            neighbors += 1
        if right < self.xscale and self.cells[right][yy].alive_curr_gen:
            neighbors += 1

        # Check vertial neighbors
        if up >= 0 and self.cells[xx][up].alive_curr_gen:
            neighbors += 1
        if down < self.yscale and self.cells[xx][down].alive_curr_gen:
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
        self._prepare_generation()

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

        self._drawfield()

    def _center_on_alive_cells(self):
        """Center the table on the alive cells"""

        # Initialize min and max to opposite extremes
        x_min = self.xscale
        x_max = 0
        y_min = self.yscale
        y_max = 0

        # Find the bounds of the alive cells
        for xx in range(self.xscale):
            for yy in range(self.yscale):
                if self.cells[xx][yy].alive_curr_gen:
                    if yy > y_max:
                        y_max = yy
                    if yy < y_min:
                        y_min = yy
                    if xx > x_max:
                        x_max = xx
                    if xx < x_min:
                        x_min = xx

        # Shift right
        while self.xscale - x_max > x_min + 1:
            x_max = x_max + 1
            x_min = x_min + 1
            self.cells.insert(0, self.cells.pop())
        else:
            # Shift left
            while x_min > self.xscale - x_max + 1:
                x_min = x_min - 1
                x_max = x_max - 1
                self.cells.append(self.cells.pop(0))

        # Shift up
        while self.yscale - y_max > y_min + 1:
            y_max = y_max + 1
            y_min = y_min + 1
            for xx in range(self.xscale):
                self.cells[xx].insert(0, self.cells[xx].pop())
        else:
            # Shift down
            while y_min > self.yscale - y_max + 1:
                y_max = y_max - 1
                y_min = y_min - 1
                for xx in range(self.xscale):
                    self.cells[xx].append(self.cells[xx].pop(0))


def setup(filename):
    """Setup table to simulate game"""
    return GameTable(640, 480, 4, filename)


def run(table):
    """Run through game of life simulation"""
    while True:
        # FIXME: Catch keyboard
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        table.advance_generation()

def teardown():
    """Stop simulating game and cleanup graphics"""
    pygame.display.quit()
    pygame.quit()


def main():
    """Main entry point for driver program"""
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    table = setup(filename)
    run(table)
    teardown()

if __name__ == "__main__":
    main()
