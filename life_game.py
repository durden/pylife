#!/opt/local/bin/python2.4

"""
Small driver program to simulate a game of Conway's life.
"""

import sys
import time
import pygame

from game import Game
from pygame.locals import QUIT


def run(game):
    """Run through game of life simulation"""
    while True:
        # FIXME: Catch keyboard
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        game.advance_generation()


def main():
    """Main entry point for driver program"""
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    game = Game(640, 480, 4, filename)
    run(game)
    game.stop()

if __name__ == "__main__":
    main()
