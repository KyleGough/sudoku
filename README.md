<h1>Logical Sudoku Solver</h1>

Logical Sudoku solver written in Python that can solve expert level 9x9 Sudoku using only logical techniques and reasoning (in other words no brute forcing, guessing or backtracking). The program outputs a detailed description of the techniques and moves required at each step to solve unique solution Sudoku. The solver reads CSV files where each puzzle can be separated by newline characters to allow batch solving. In-depth analysis is provided regarding techniques, difficulty and processing time.

View additonal information on the logical techniques used [here](https://www.kylegough.co.uk/projects/sudoku).

## Table of Contents
- [Screenshot](#screenshot)
- [Techniques](#techniques)
- [Benchmarking and Testing](#benchmarking-and-testing)
- [Technique Coverage and Occurrences](#technique-coverage-and-occurrences)
- [Datasets](#datasets)
- [Running](#running)

## Screenshot
![combined](https://user-images.githubusercontent.com/24881448/193449962-787836fd-ca46-4592-b112-45d83fdcfb5a.png)

## Techniques
- Solo Candidate
- Hidden Candidate
- Subset Cover
- Pointing Pairs/Triples
- Box/Line Intersection
- X-Wing
- Singles Chain
- Y-Wing
- Unique Rectangles
- Swordfish
- Jellyfish
- Bi-Value Universal Grave
- XYZ-Wing
- WXYZ-Wing

## Benchmarking and Testing
Accuracy is determined by applying the corresponding technique and all previous techniques across all 49,151 17-clue Sudokus.

| Technique                | Tests Passed ( /49,151) | Tests Passed (%) |
| ------------------------ | ----------------------- | ---------------- |
| Solo Candidate           | 0                       | 0                |
| Hidden Candidate         | 21,905                  | 44.6             |
| Subset Cover             | 34,269                  | 69.7             |
| Pointing Pairs           | 41,376                  | 84.2             |
| Box/Line Reduction       | 41,628                  | 84.7             |
| X-Wing                   | 41,643                  | 84.7             |
| Singles Chain            | 44,597                  | 90.7             |
| Y-Wing                   | 45,798                  | 93.2             |
| Unique Rectangles        | 45,885                  | 93.3             |
| Swordfish                | 45,907                  | 93.4             |
| Jellyfish                | 45,912                  | 93.4             |
| Bi-Value Universal Grave | 46,118                  | 93.8             |
| XYZ-Wing                 | -                       | -                |
| WXYZ-Wing                | -                       | -                |

## Technique Coverage and Occurrences

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
| Swordfish          | 0.2          | 138         |
| Jellyfish          | 0.0          | 7           |
| BUG                | 0.4          | 204         |
| XYZ-Wing           | 0.8          | 419         |
| WXYZ-Wing          | 0.7          | 359         |

## Datasets

Datasets of different Sudoku puzzles were tested against the solver in order to test completeness, speed and efficiency.

- [Gordon Royle's list of all currently known 17-clue minimal Sudoku puzzles](http://staffhome.ecm.uwa.edu.au/~00013890/sudokumin.php)
  <br />Used as the primary benchmark as contains a wide range of puzzle difficulties. 17 clues (initial numbers on the grid) is the minimum number of clues any Sudoku can have such that it has a unique solution. Testing all 49,151 puzzles repeatedly is time-consuming, so a subset of 1000 of these puzzles are used for continual testing purposes. Testing of all 49,151 is performed when relevant milestones are reached.
- [1 million Simple Sudoku games](https://www.kaggle.com/bryanpark/sudoku)
  <br />The solver successfully solves 100% of the Sudoku in this dataset. A subset of 1000 of these puzzles are used to check for errors during development.

## Running

The solver will run on `.csv` files where each 81-character line can represent one puzzle. 0's represent missing/unknown cells and the order of the cells goes from top to bottom, left to right. This project provides some example `.csv` files to test the program, for example to test the program on some Sudoku which require the use of the x-wing technique to solve, run:

```
./sudoku -om tests/xwing.csv
```

- Use the `-m` flag to display the techniques used at each stage of solving.
- Use the `-o` flag to display the initial grid and solved grid.
