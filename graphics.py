#!/opt/local/bin/python2.4

"""
Module to serve as a graphics library for pylife game simulation.
"""

import Numeric
import pygame


class Graphics(object):
    """Class handle graphics of pylife engine.  This class could (hopefully) be
    easily overidden to support different types of graphics such as ncurses,
    ascii art, etc.

    To implement your own graphics front-end with the pylife engine you should
    do the following:
        1. Subclass Graphics class OR Create your own Graphics class
        2. Implement the initializer (width, height) for dimensions of board
        3. Implement draw() method to draw your graphics
        4. Implement cleanup() to handle any cleanup when game stops
    """

    def __init__(self, width, height, xscale, yscale):
        """Setup graphics (game board) with given dimensions"""
        pygame.init()

        self.scale_screen = None
        self.screen = None

        self.xscale = xscale
        self.yscale = yscale

        # 2-D array that cooresponds to pixels on surface
        self.px_arr = Numeric.zeros((self.xscale, self.yscale), 'i')

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

    def draw(self, cells):
        """Draw board with given cells (of type pylife.game.cell)"""

        self._color_cells(cells)

        pygame.surfarray.blit_array(self.scale_screen, self.px_arr)
        temp = pygame.transform.scale(self.scale_screen,
                                        self.screen.get_size())
        self.screen.blit(temp, (0, 0))
        pygame.display.update()

    def cleanup(self):
        """Stop simulating game and cleanup graphics"""
        pygame.display.quit()
        pygame.quit()

    def _color_cells(self, cells):
        """Setup the color of all given cells"""
        for xx in range(self.xscale):
            for yy in range(self.yscale):
                cells[xx][yy].alive_curr_gen = \
                    cells[xx][yy].alive_next_gen

                color = 0
                if cells[xx][yy].generation_cnt > 0:
                    if cells[xx][yy].generation_cnt >= 4:
                        color = 4
                    else:
                        color = cells[xx][yy].generation_cnt

                self.px_arr[xx][yy] = color
