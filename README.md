# Sudoku Logical Solver
A logical Sudoku solver that outputs the techniques and moves required at each step to solve the puzzle. No backtracking or brute forcing will be used.



### Testing:

Datasets of different Sudoku puzzles were tested against the solution in order to test completeness, speed and efficiency.

- 1 million Sudoku games - https://www.kaggle.com/bryanpark/sudoku
  - All Sudokus in this dataset are 'simple'. The solver successfully solves 100% of the items in this dataset.
- Gordon Royle's list of all known 17-clue Sudoku puzzles - http://staffhome.ecm.uwa.edu.au/~00013890/sudokumin.php
  - The solver currently solves **78.7%** of the Sudokus in this dataset. Currently the goal is to achieve 80%+ by implementing new strategies.



### Techniques:

##### Single Candidate #####

##### Hidden Candidate ###

##### Hidden/Unique Pairs/Triples/Quads #####

##### Pointing Pairs #####

##### Box/Line Intersection #####

##### X-Wing #####

##### Swordfish #####