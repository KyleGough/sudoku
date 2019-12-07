# Logical Sudoku Solver


A logical Sudoku solver that outputs the techniques and moves required at each step to solve the puzzle. No backtracking or brute forcing will be used. The solver can read .csv files to solve multiple puzzles in a batch.



## Implemented Techniques ##



##### Single Candidate #####

```
A cell can only be on possible value.
```

Using only this strategy is not sufficient enough to solve any 17-clue Sudokus



##### Hidden Candidate ###

```
Where a value is only valid in one cell within a column, row or sector. 
```

Using only the *Single Candidate* and *Hidden Candidate* techniques, *44.6%* of the 49,151 17-clue Sudokus were solved.



##### Subset Cover (Hidden/Unique Pairs/Triples/Quads) #####

``` 
Subsets of pairs/triples/quads to remove possibilities.
```

 Implementing the *Subset Cover* technique boosted the accuracy by over *20%* up to *68.6%*.



##### Pointing Pairs #####

```
Uses pairs or triples of possible values in a sector that are on the same row/column to eliminate possibilities in the same row/column.
```

Implementing the *Pointing Pairs* technique boosted the accuracy by *8.9%* up to *77.5%*. 



##### Box/Line Intersection #####

``` 
Uses pairs or triples of a value along a row/column that are all in the same sector to remove other possibilities in the sector.
```

Implementing the *Box/Line Reduction* technique boosted the accuracy by *0.3%* up to *77.8%*.



##### X-Wing #####

``` 
Values restricted in 2 places along a column in 2 columns that all share the same rows.
```

MORE...



##### Swordfish #####



##### MORE... #####



##### Summary #####

| Technique          | Accuracy on 49,151 17-clue dataset |
| ------------------ | ---------------------------------- |
| Solo Candidate     | 0.0%                               |
| Hidden Candidate   | 44.6%                              |
| Subset Cover       | 68.6%                              |
| Pointing Pairs     | 77.5%                              |
| Box/Line Reduction | 77.8%                              |

*Note: Accuracy is determined by applying the corresponding technique and all previous techniques.*



## Testing ##



Datasets of different Sudoku puzzles were tested against the solution in order to test completeness, speed and efficiency.

- [1 million Simple Sudoku games][1]
  - All Sudokus in this dataset are 'simple'. The solver successfully solves 100% of the items in this dataset.
- [Gordon Royle's list of all known 17-clue Sudoku puzzles][2]
  - 17 clues (initial numbers on the grid) is the minimum number of clues any Sudoku can have. The solver currently solves *78.7%* of the Sudokus in this dataset. Currently the goal is to achieve 80%+ by implementing new strategies. Testing all 49,151 puzzles is time-consuming, so a subset of 1000 of these puzzles are used for continual testing purposes.
- MORE...



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