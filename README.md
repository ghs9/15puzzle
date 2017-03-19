# 15puzzle
## AI demo for 15 puzzle

### To run:

1) Download python 2.7
2) Run 15puzzle.py from command line with the following arguments.
  * “[initialstate]” [searchmethod] [options] 
  * [initialstate] must contain sixteen characters, namely the digits 1-9, letters AF, and a space, in any order. • [searchmethod] can be: BFS, DFS, DLS, ID, GBFS, AStar.
  * [options] are only relevant for DLS (depth-limited search), where the option specifies the maximum depth to explore, GBFS and AStar, where the option specifies which heuristic to use.
  * Examples: 
    * “123456789AB DEFC” BFS
    * “123456789AB DEFC” DFS
    * “123456789AB DEFC” DLS 2
    * “123456789AB DEFC” GBFS h1
    * “123456789AB DEFC” AStar h2 

### Demonstrates the following search algorithms:

* Breadth-first search
* Depth-first search
* Greedy best first search
  * Heuristic 1 which is the number of misplaced pieces.
  * Heuristic 2 which is the manhattan distance of all pieces to their correct places
* A\* Search
  * Heuristic 1 which is the number of misplaced pieces.
  * Heuristic 2 which is the manhattan distance of all pieces to their correct places
* Depth-limited search
* Uniform-cost search
