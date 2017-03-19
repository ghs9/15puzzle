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
3) Output is in the following form
 *[depth], [numCreated], [numExpanded], [maxFringe] 
 *[depth] represents the depth in the search tree where the solution is found. The integer will be zero if the solution is at the root and it will be “-1” if a solution was not found.
 * [numCreated] is the counter that is incremented every time a node of the search tree is created (output 0 if depth == -1).
 * [numExpanded] is the counter that will be incremented every time the search algorithm acquires the successor states to the current state; i.e. every time a node is pulled off the fringe and found not to be the solution (output 0 if depth == -1).
 * [maxFringe] is the maximum size of the fringe at any point during the search (output 0 if depth == -1).
 * Example: 
   * java FifteenProblem "123456789ABC DFE" BFS 
         3, 54, 17, 37

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
