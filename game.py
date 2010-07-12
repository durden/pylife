#!/opt/local/bin/python2.4

"""
Module to handle logic of simulating Conway's Game of Life.

This module requires a graphics library, graphics.py.  However, this library
can be overidden to provide different types of graphics.  See graphics.py for
details.
"""

import graphics as graphics_lib


class Cell(object):
    """Individual cell"""

    def __init__(self):
        self.alive_curr_gen = False
        self.alive_next_gen = False
        self.generation_cnt = 0


class Game(object):
    """Class to handle simulating game of life"""

    def __init__(self, width, height, scale, seed_file=None):
        self.cells = []

        self.xscale = width / scale
        self.yscale = height / scale

        # Create 2-D list of cells to handle all pixels
        for xx in range(self.xscale):
            self.cells.append([])
            for yy in range(self.yscale):
                self.cells[xx].append(Cell())

        self._init_configuration(seed_file)
        self._center_on_alive_cells()

        self.graphics = graphics_lib.Graphics(width, height, self.xscale,
                                                self.yscale)
        self.advance_generation()

    def advance_generation(self):
        """Advance all cells by 1 generation"""
        self._prepare_generation()
        self.graphics.draw(self.cells)

    def stop(self):
        """Quit game simulation and cleanup"""
        self.graphics.cleanup()

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
                if yy > self.yscale:
                    raise IOError("File height (%d) too large for game " \
                                    "table height (%d)" % (yy, self.yscale))
                for char in line:
                    if xx > self.xscale:
                        raise IOError("File width (%d) too wide for game" \
                                        "table width (%d)" % (xx, self.xscale))
                    if char == "O":
                        self.cells[xx][yy].alive_curr_gen = True
                    xx = xx + 1
                xx = 0
                yy = yy + 1

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

        # Check top diagonal neighbors
        if left >= 0 and up >= 0 and self.cells[left][up].alive_curr_gen:
            neighbors += 1
        if right < self.xscale and up >= 0 and \
                self.cells[right][up].alive_curr_gen:
            neighbors += 1

        # Check bottom diagonal neighbors
        if left >= 0 and down < self.yscale and \
                self.cells[left][down].alive_curr_gen:
            neighbors += 1
        if right < self.xscale and down < self.yscale and \
                self.cells[right][down].alive_curr_gen:
            neighbors += 1

        return neighbors

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
