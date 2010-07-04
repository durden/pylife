This is my quick python implementation of
[Conway's Game of Life](http://en.wikipedia.org/wiki/Conway's_Game_of_Life).

## Requirements/Limitations:

- Hard-coded to use python 2.4 and hard-coded python location (I'm using
  macports to get pygame working with OS 10.6)
- Pygame1.9 (via macports)
- Numeric (via macports)

## Todo items:

- Allow board dimensions and scale to be specified via command line.
- Move game classes into separate module to allow for writing simple.
  simulations without worrying about underlying game code
- Don't force simulation code to know about pygame module
- More colors
- Start/stop buttons on screen
- Unit tests for game code
