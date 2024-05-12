# sudokuSolveAI

## Problem Statement
Given a 9x9 Sudoku Puzzle as a Constraint Satisfaction Problem (“CSP”), the program outputs a complete and consistent assignment.
## What is Sudoku?
## Implementation - Dictionary

For the dictionary based implementation, we used the following dictionaries:
- Domains: This dictionary contains the variable (i.e., the row and column identified by a
letter and number respectively) a key and the domain (i.e., a list of domain values) as the
key’s value.
- Assignments: Similar to the first dictionary, this dictionary contains the variable as a key
and its assigned value as the value. Variables that do not have a value assigned to them
hold a 0 as the value. 0 was chosen since the actual domain for a variable in the sudoku
puzzle is restricted to numbers from 1 to 9. There is an evaluative function that checks if
the assignments for a variable are consistent with the constraints dictionary discussed
below.
- Constraints: Similar to the previous dictionary, this dictionary contains the variable as the
key and the constraints for the respective variable in a list. Each constraint (item) in the
list of constraints is of type string. There is an evaluative function that iterates over the
assignments dictionary given a list of variables (used as keys while iterating) and
determines if they meet the constraints.
- In addition to the previous three dictionaries, we also had a dictionary called indexes.
This contained the index of each variable (i.e., cell in sudoku puzzle) as the value for any
variable which is the key. Although this is outputted when the function loadSudoku() was
called, we did not use it anywhere in the program.
## AC-3 and Revise Implementation
For the data structure based implementation, AC-3 generated a queue. The queue was in-essence
a list that contained all the edges. Following the initialization of the queue, a while loop was
entered, and until the queue was empty, each edge from the queue was popped, assigned to a
variable called arc, and had the function revise() called upon it. Revise would then loop through
the edges associated constraints and trim the from_nodes domain. In the dictionary based
implementation, since the number of elements in the queue reduced linearly, we decided that there was no need to use a graph and edge system. Instead, we iterated over the list of variables
in AC-3 and called revise on each of the variables. Without elaborating on the logic
specifications, revise simply just iterated over the constraints for the given variable and trimmed
its domain.
## Backtracking Implementation
All the implementations of backtracking used AC-3 for inference. The data structure based
implementation followed the pseudocode provided by the m5-csp slides and called AC-3
directly. Unfortunately, the latter failed due to reference related issues. When we parsed data
structures to the recursive calls of backtracking, it was relatively difficult to debug bugs that
were encountered. Additionally, the inference calls made changes directly to the data structure
and there was an issue related to assigning values to variables. To avoid this issue, we used
dictionaries. With the dictionary based implementation, we used deepcopy (i.e., pass by value
rather than reference) to ensure that each recursive call used a unique copy of the three
dictionaries discussed above. Additionally, we wrote a separate infer function which extended
the AC-3 algorithm to operate on deep copies of the parameters (i.e., the three dictionaries). This
resolved the problem we encountered with data structures.
## Conclusion
Therefore, the dictionary based implementation of AC-3, revise, and backtrack-search is able to
solve any sudoku given as an input in a matter of seconds. Please download the attached .zip file
to view the code for the dictionary based implementation (required dependencies: numpy,
pygame).

