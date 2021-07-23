# Maze-solver
This uses Q learning to move a player around a maze.

To run the program first add maze to PYTHONPATH. 
```export PYTHONPATH=<absolute_path_to_maze_directory>:$PYTHONPATH.```

Run the `grid.py` program.

1. `maze/grid.py --interactive [--random]`: Use arrow keys to move around a maze. use `--random` flag to generate random mazes.

1. `maze/grid.py --q [--random]`: An &epsilon;-greedy Q-learner
   repeatedly runs the maze. The parameters are not tuned to learn
   quickly. Over the course of several minutes the player first learns
   to avoid spikes, then reach the treasure, and eventually reach the
   treasure in the minimum number of steps.

1. `maze/all_tests.py`: Run the unit tests.
