# CoRoutineWorld

A Python-based 2D grid-based world with modifiable state in each cell of the grid.

The world evolves by iterating over instructions.
The instructions iterator is a coroutine, which`yield`s instructions for how a cell should transition,
and receives information about neighboring cells via `send`.

The world, while implemented as a grid, loops infinitely, just like the surface of a sphere (e.g. Planet Earth).
This means that each cell always has 4 neighbors (North, East, South, West) - there are no "boundary cells". 