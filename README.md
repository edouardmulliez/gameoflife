# Game of Life

This is an implementation of **James Conway's game of life**.

## The Rules

For a space that is *populated*:
- Each cell with one or no neighbors dies, as if by solitude.
- Each cell with four or more neighbors dies, as if by overpopulation.
- Each cell with two or three neighbors survives.

For a space that is *empty*:
- Each cell with three neighbors becomes populated.

