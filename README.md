# Logical Sudoku Solver (W.I.P.)

A logical Sudoku solver that analyses the techniques and moves required at each step to solve the puzzle. No backtracking or brute forcing will be used. The solver can read *.csv* files to solve multiple puzzles in a batch. Simple difficulty analysis has been implemented based on the number of moves requires, initial clues and technical strategies required to solve the puzzle.



## Strategies/Techniques ##



##### Single Candidate #####

- A cell can only be one possible value.

Using only this strategy is not sufficient enough to solve any 17-clue Sudokus



##### Hidden Candidate ###

- Where a value is only valid in one cell within a column, row or sector. 

Using only the *Single Candidate* and *Hidden Candidate* techniques, *44.6%* of the 49,151 17-clue Sudokus were solved.



##### Subset Cover (Pairs/Triples/Quads) #####

- Subsets of pairs/triples/quads. N cells that cover N different values within a row/column/sector can be used to eliminate possibilities. 2 <= N <= 4.

 Implementing the *Subset Cover* technique boosted the accuracy by over *20%* up to *68.6%*.



##### Pointing Pairs #####

- Uses pairs or triples of possible values in a sector that are on the same row/column to eliminate possibilities in the same row/column.

Implementing the *Pointing Pairs* technique boosted the accuracy by *8.9%* up to *77.5%*. 



##### Box/Line Intersection #####

- Uses pairs or triples of a value along a row/column that are all in the same sector to remove other possibilities in the sector.

Implementing the *Box/Line Reduction* technique boosted the accuracy by *0.3%* up to *77.8%*.



##### X-Wing #####

- Single value chaining strategy. Values restricted in 2 places along a column in 2 columns that all share the same rows can help eliminate values.



##### Summary #####

| Technique          | Accuracy on Gordon Royle's 49,151 17-clue dataset |
| ------------------ | ------------------------------------------------- |
| Solo Candidate     | 0.0%                                              |
| Hidden Candidate   | 44.6%                                             |
| Subset Cover       | 68.6%                                             |
| Pointing Pairs     | 77.5%                                             |
| Box/Line Reduction | 77.8%                                             |

*Note: Accuracy is determined by applying the corresponding technique and all previous techniques.*



## Benchmarking and Testing ##



Datasets of different Sudoku puzzles were tested against the solution in order to test completeness, speed and efficiency.

- [Gordon Royle's list of all known 17-clue Sudoku puzzles][2]
  - 17 clues (initial numbers on the grid) is the minimum number of clues any Sudoku can have.
  - The solver currently solves *78.7%* of the Sudokus in this dataset. Currently the goal is to achieve 80%+ accuracy across the whole set by implementing new strategies.
  - Testing all 49,151 puzzles is time-consuming, so a subset of 1000 of these puzzles are used for continual testing purposes.
  - This dataset will be used as the primary benchmark.

- [1 million Simple Sudoku games][1]
  - All Sudokus in this dataset are 'simple'. The solver successfully solves 100% of the items in this dataset.
  - A subset of 1000 of these puzzles are used to check for errors.



![image-20191208161251656](/home/kyle/.config/Typora/typora-user-images/image-20191208161251656.png)



Here is a partially solved Sudoku:

* Cells with only one value (Yellow/Purple) are cells which the value is known to be the value in the cell.

* Cells with one or more values (Blue/Red) are cells which the value could be one of the values in the cell.
* Different colours are used to differentiate between the 3x3 sectors.



## Example Output



<img src="/home/kyle/Pictures/sudoku-moves-1.png" alt="sudoku-moves-1" style="zoom: 67%;" />



At each step the following information is output:

* Techniques used to gain information.
* Cells and structures used to gain information.
* Cells it affects.



## Getting Started ##



#### Installing and Running ####

Clone the repository.

``` bash
git clone https://github.com/KyleGough/sudoku.git
```



Change into the directory.

``` git
cd sudoku
```



Run the solver on 1000 simple Sudoku.

``` git
python solver.py datasets/simple-1000.csv
```



The output should look something like this.

```
[ Tests ]
 - Solved 1000 out of 1000 tests. (100.0%)
```



## References ##

[1]: https://www.kaggle.com/bryanpark/sudoku	"1,000,000 Sudoku"
[2]: http://staffhome.ecm.uwa.edu.au/~00013890/sudokumin.php	"17-Clue Sudokus"
