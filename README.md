# Logical Sudoku Solver

CLI logical Sudoku solver that can solve expert level 9x9 Sudoku using only logical techniques and reasoning (in other words no brute forcing, guessing or backtracking). The program outputs a detailed description of the techniques and moves required at each step to solve unique solution Sudoku. The solver reads csv files where each puzzle can be separated by newline characters to allow batch solving. After processing all Sudoku in a given file, in-depth analysis is displayed including but not limited to: difficulty rating, occurrences of each technique, probability of each technique, processing time for each technique and total processing time.

![Sudoku Solver](./images/results)

------

## Terminology

* **Candidates** - The possible values a cell can be. Various techniques will aim to reduce to number of candidates for each cell using logical reasoning.
* **Simple Sudoku** - A Sudoku that can be solved only using the solo candidate and hidden candidate techniques.
* **Minimum Sudoku** - A Sudoku where removing a clue from the initial configuration produces a Sudoku without a unique solution. Minimum Sudoku must have at least 17 clues.
* **Conjugate Pair** - Where a candidate is only valid in exactly two cells within a structure, the two cells form a conjugate pair.
* **Weak Pair** - Two cells part of two different conjugate pairs that share the same row, column or sector.

------

## Solution Techniques ##

##### Solo Candidate #####

The *solo candidate* technique is a simple technique for identifying the value of cells where a cell has only one candidate, therefore the cell must be that candidate. This technique has been implemented using a **O(N<sup>2</sup>)** complexity algorithm as every cell in the grid must be checked. Multiple solo candidates can be observed in one pass of the algorithm. Using only this strategy is not sufficient enough to solve any 17-clue Sudoku.


##### Hidden Candidate ###

The *hidden candidate* technique is another simple technique for identifying the value of cells. If a candidate is valid in only one cell within a column, row or sector then that cell must be that value. This technique has been implemented using a **O(N<sup>3</sup>)** complexity algorithm as each cell in a structure (column, row, sector) must be checked against each candidate. Using only the *Single Candidate* and *Hidden Candidate* techniques, *44.6%* of the 49,151 17-clue Sudoku were solved. However, these two strategies are sufficient enough to solve every simple Sudoku.



##### Subset Cover (Pairs/Triples/Quads/Quints) #####

The *subset cover* technique eliminates candidates within a column, row or sector. If a subset of *N* cells within a structure covers *N* different candidates (i.e. union of candidates in the *N* cells is of size *N*) then the candidates must be contained within these *N* cells and cannot appear elsewhere in the structure. This technique is only valid for *2<=N<=5* as any subset of size *N* greater than 5 will automatically be composed of a smaller subset of size *(9-N)* which will be simpler to solve.



##### Pointing Pairs/Triples #####

The *pointing pairs/triples* technique eliminates candidates within a column or row. If a candidate occurs either two or three times within a sector and these cells are all within the same column/row, then the value must be located within the sector and cannot occur elsewhere the column/row. This technique has been implemented using a **O(N<sup>3</sup>)** complexity algorithm as each cell in every sector must be checked for each candidate.



##### Box/Line Intersection #####

The *box/line intersection* technique eliminates candidates within a sector. If a candidate value in a column/row only appears within one sector, then that candidate must occur in the sector in that column/row, and so the candidate can be eliminated from the other cells in the same sector. This technique has been implemented using a **O(N<sup>3</sup>)** complexity algorithm as each cell in a column/row must be checked for every column/row.



##### X-Wing #####

The *X-Wing* technique is a subset of single value chaining strategies where a candidate is restricted in two cells along a column in two different columns that all share the same rows. The technique can also be expressed as two conjugate pairs joined by two weak links where the four cells form a rectangle. This technique has been implemented using a **O(N<sup>3</sup>)** complexity algorithm.



##### Singles Chain

The *singles chain* technique firstly identifies for a given candidate all the conjugate pairs. Then constructs a connected graph of conjugate pairs with nodes of alternating state (ON/OFF). The conjugate pairs are used to find either violations of cells in the graph (two cells of the same state that are in the same structure) or cells not in the graph that can see nodes of both states. This technique has been implemented using an adjacency list to store the graph on conjugate pairs leading to an algorithmic complexity of **O(N<sup>3</sup>)**.



##### Y-Wing

The *Y-Wing* technique is a bi-value chaining strategy that uses three bi-value cells to eliminate candidates. The head of the Y-Wing has candidates AB, there are two wings that share the same structure as the head with candidates AC and BC respectively. Whatever the actual value of the head, either wing must be C. Therefore any cells that intersect with both wings can remove C as a candidate. This technique has been implemented using a **O(N<sup>3</sup>)** complexity algorithm.



##### Unique Rectangles

The *Unique Rectangle* technique eliminates candidates by preventing a state where there exist multiple solutions. A *Unique Rectangle* is a group of four cells that form a rectangle of which the cells occupy exactly two sectors. Additionally, three of the cells in the rectangle must be AB and the remaining cell must contain at least AB. This cell cannot be A or B as it would form a rectangle where the A or B are interchangeable.



##### Swordfish

The *Swordfish* technique is an extension of the *X-Wing* technique but where a candidate is restricted in three cells along a column in three different columns that all share the same rows.



##### Jellyfish

The *Jellyfish* technique is an extension of both the *X-Wing* and *Swordfish* techniques, but with a candidate restricted in four cells along a column in four different columns that all share the same rows.



##### Bi-Value Universal Grave

The *Bi-Value Universal Grave* (BUG) is a state that a Sudoku can reach where all unsolved cells in the Sudoku have only 2 candidates, except a single cell that has 3 candidates. The aim of this technique to detect the BUG state and use it to eliminate candidates. This technique has been implemented using a **O(N<sup>2</sup>)** complexity algorithm.



##### XYZ-Wing

The *XYZ-Wing* technique is an extension of the *Y-Wing* technique but with the head containing 3 candidates instead of 2. The head of the XYZ-Wing has candidates XYZ, there are two wings that share the same structure as the head with candidates XZ and YZ respectively. Any cells that intersect with all 3 cells of the XYZ-Wing cannot contain the candidate Z. This technique has been implemented using a **O(N<sup>3</sup>)** complexity algorithm.



##### WXYZ-Wing

The *WXYZ-Wing* technique is a further extension of *Y-Wing* and *XYZ-Wing* but with the head containing 4 candidates and three wings that share candidates with the head and have a single common candidate between all 4 cells. If all cells in the *WXYZ-Wing* have candidate Z, then candidate Z can be removed from every cell that intersects with all 4 cells of the *WXYZ-Wing*.



##### Future Work

I have implemented only a few logical techniques, however there are far more complex and advanced techniques available but occur very rarely in practice. I may implement additional techniques as I come to understand them. Unfortunately I cannot hope to be able to solve all known Sudoku as solving all using only logical techniques is still an incomplete problem.



------



## Benchmarking and Testing ##



##### Summary #####

| Technique                | Tests Passed ( /49,151) | Tests Passed (%) |
| ------------------------ | ----------------------- | ---------------- |
| Solo Candidate           | 0                       | 0                |
| Hidden Candidate         | 21,905                  | 44.6             |
| Subset Cover             | -                       | -                |
| Pointing Pairs           | 41,302                  | 84.0             |
| Box/Line Reduction       | 41,577                  | 84.6             |
| X-Wing                   | 41,594                  | 84.6             |
| Singles Chain            | 44,530                  | 90.6             |
| Y-Wing                   | 45,732                  | 93.0             |
| Unique Rectangles        | -                       | -                |
| Swordfish                | -                       | -                |
| Jellyfish                | -                       | -                |
| Bi-Value Universal Grave | 45,929                  | 93.4             |
| XYZ-Wing                 | -                       | -                |
| WXYZ-Wing                | 46,265                  | 94.1             |

*Note: Accuracy is determined by applying the corresponding technique and all previous techniques across all 49,151 17-clue Sudokus.*





##### Coverage and Total Occurrences

This table demonstrates the percentage of test puzzles that feature at least one of each technique. Note that some harder techniques could be employed instead of multiple uses of easier techniques in certain Sudoku, however the solver has been implemented to ensure that easier techniques are prioritised over the more difficult techniques. 

| Technique          | Coverage (%) | Occurrences |
| ------------------ | ------------ | ----------- |
| Solo Candidate     | 98.6         | 384,825     |
| Hidden Candidate   | 100.0        | 271,095     |
| Subset Cover       | 49.0         | 58,202      |
| Pointing Pairs     | 25.3         | 14,211      |
| Box/Line Reduction | 2.7          | 1,416       |
| X-Wing             | 0.8          | 412         |
| Singles Chain      | 8.1          | 4,752       |
| Y-Wing             | 3.0          | 1,279       |
| Unique Rectangles  | -            | -           |
| Swordfish          | 0.2          | 138         |
| Jellyfish          | 0.0          | 7           |
| BUG                | 0.4          | 204         |
| XYZ-Wing           | 0.8          | 419         |
| WXYZ-Wing          | 0.7          | 359         |





##### Datasets

Datasets of different Sudoku puzzles were tested against the solver in order to test completeness, speed and efficiency.



- [Gordon Royle's list of all currently known 17-clue minimal Sudoku puzzles][2]
  - 17 clues (initial numbers on the grid) is the minimum number of clues any Sudoku can have such that it has a unique solution.
  - ~~Currently the goal is to achieve 90+% accuracy across the whole set by implementing new strategies.~~
  - Testing all 49,151 puzzles repeatedly is time-consuming, so a subset of 1000 of these puzzles are used for continual testing purposes. Testing of all 49,151 is performed when relevant milestones are reached.
  - This dataset will be used as the primary benchmark as the dataset contains a wide range of puzzle difficulties.




- [1 million Simple Sudoku games][1]
  - All Sudokus in this dataset are simple (require only solo candidate and hidden candidate to solve).
  - The solver successfully solves 100% of the Sudoku in this dataset.
  - A subset of 1000 of these puzzles are used to check for errors during development.





Here is a partially solved Sudoku:

* Cells with only one value (Yellow/Purple) are cells which the value is known to be the value in the cell.

* Cells with one or more values (Blue/Red) are cells which the value could be one of the values in the cell.
* Different colours are used to differentiate between the 3x3 sectors.



------



## Example Output



At each step the following information is output:

* Techniques used to gain information and what deductions have been made.
* Cells and structures used to gain information.
* Cell(s) it affects.



![exampleoutput](/home/kyle/Documents/sudoku/images/exampleoutput.png)



At the end of execution the following is output.

* Percentage of tests solved.
* Percentage of tests exhausted - *Tests which were not solved.*
* Percentage of tests that encountered errors - *Hopefully should be 0%.*
* Mean number of clues in the provided puzzles.
* Mean, minimum, and maximum difficulty scores for the test puzzles.
* For each technique the following is output:
  * *(i)* True or False: whether or not the technique was encountered.
  * *(ii)* Number of occurrences of the technique.
  * *(iii)* Percentage of puzzles the technique is used in.  
  * *(iv)* Number of solved puzzles the technique was used at least once on.
  *  *(v)* Total execution time in seconds processing the technique. The top 3 longest duration techniques are coloured red, the top 5 are coloured yellow, whilst the remaining techniques are coloured green.
* Total time elapsed in seconds.
* Mean time elapsed per puzzle.



------



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
./sudoku tests/simple-1000.csv
```



The output should look something like this.

```
[ Tests ]
 - Solved 1000 out of 1000 tests. (100.0%)
```

There are two optional flags:

* `-m` - Displays the moves and techniques used at each stage of solving the Sudoku.
* `-o` - Displays the initial grid and solution in the terminal.


`./sudoku -m -o tests/simple-1000.csv`

------



## References ##

[1]: https://www.kaggle.com/bryanpark/sudoku	"1,000,000 Sudoku"
[2]: http://staffhome.ecm.uwa.edu.au/~00013890/sudokumin.php	"17-Clue Sudoku"
