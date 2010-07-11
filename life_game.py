#!/opt/local/bin/python2.4

"""
Small driver program to simulate a game of Conway's life.
"""

import time
from optparse import OptionParser

from game import Game


def run(game, secs):
    """Run through game of life simulation, sleeping secs between
       generations
    """
    while True:
        time.sleep(secs)
        game.advance_generation()


def get_args():
    """Setup arguments"""
    parser = OptionParser()

    parser.add_option("-f", "--file", dest="filename",
                        help="File to populate initial alive cells",
                        metavar="FILE", default=None)

    parser.add_option("-t", "--secs", dest="secs",
                        help="Time (in seconds) between generations "
                        "(decimals allowed)", default=1, type="float")

    (options, args) = parser.parse_args()
    return options


def main():
    """Main entry point for driver program"""

    options = get_args()

    # Python 2.4 doesn't allow except and finally clause together, so must
    # wrap with outer finally instead
    try:
        # Run game and always allow library to cleanup when user exits
        try:
            game = Game(640, 480, 4, options.filename)
            run(game, options.secs)
        # Catch keyboard so ctrl-c doesn't show nasty stack trace
        except KeyboardInterrupt:
            pass
    finally:
        game.stop()

if __name__ == "__main__":
    main()
