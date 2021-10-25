# CoRoutineWorld

A Python-based 2D grid-based world with modifiable state in each cell of the grid.

> :warning: **WARNING**: Currently only one primitive, MoveIfY, is implemented.


## About

The world evolves by iterating over the communications provided by `interface`.
`interface` is a coroutine, which directly updates the state of a cell,
and receives information about the world via `send`.

The world, while implemented as a grid, loops infinitely, just like the surface of a sphere (e.g. Planet Earth).
This means that each cell always has 4 neighbors (North, East, South, West) - there are no "boundary cells". 