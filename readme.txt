Place game.py and main.py in the same directory

In main.py:
- you can change the 'input_case' variable on line 5 to either 'A', 'B', or 'C' depending on which initial state test case you want to run the code on.
- you can change the 'heuristic_choice' variable on line 6 to 0 for uniform-cost search, 1 for heuristic 1, or 2 for heuristic 2 to be used.

Run main.py. 
- If the puzzle is solvable, it will print a minimal-length sequence of states from initial state to a goal state, as well as the path-length and the number of states that were goal-tested.
- If the puzzle is unsolvable, it will tell you so.

Interpreting the results:
- In the grid, each distinct letter corresponds to a different vehicle. A capital letter indicates that cell being occupied by the trunk (far back) of the vehicle, and the other cells occupied are lowercase.