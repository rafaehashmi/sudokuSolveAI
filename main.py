from copy import deepcopy as asvalue

import numpy as np

from constants import *


def assignToBoard(variables, assignments):
    """
    Assigns values to a temporary matrix representing the Sudoku board based on the variable assignments.

    Args:
        variables (list): A list of variables representing the Sudoku board positions.
        assignments (dict): A dictionary containing the variable assignments.

    Returns:
        list: A temporary matrix representing the Sudoku board with assigned values.
    """
    # Create a temporary matrix to represent the Sudoku board
    tempMat = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # Assign values to the temporary matrix based on the variable assignments
    for variable in variables:
        tempMat[rowLetterKey[variable[0]]][int(variable[1]) - 1] = assignments[variable]
    return tempMat


def viewBoard(variables, assignments):
    """
    Print the Sudoku board based on the variable assignments.

    Parameters:
    - variables (list): A list of variables representing the Sudoku board.
    - assignments (list): A list of assignments for the variables.

    Returns:
    None
    """
    # Print the Sudoku board based on the variable assignments
    print(np.array(assignToBoard(variables, assignments)))
    return


def genboxConstraints():
    """
    Generate box constraints for each box in the Sudoku board.

    This function generates box constraints for a given range of rows and columns in the Sudoku board.
    It writes the constraints to a file named "map_constraints.txt".

    Parameters:
    None

    Returns:
    None
    """

    def genboxConstraintsHelper(x, y, w, z):
        # Generate box constraints for a given range of rows and columns
        with open("map_constraints.txt", "a+") as f:
            for i in range(x, y):
                for j in range(w, z):
                    for k in range(x, y):
                        for l in range(w, z):
                            if (k, l) != (i, j):
                                f.write(
                                    f"{rowIndexKey[i]}{j+1}!={rowIndexKey[k]}{l+1}\n"
                                )

    # Generate box constraints for each box in the Sudoku board
    genboxConstraintsHelper(0, 3, 0, 3)
    genboxConstraintsHelper(0, 3, 3, 6)
    genboxConstraintsHelper(0, 3, 6, 9)
    genboxConstraintsHelper(3, 6, 0, 3)
    genboxConstraintsHelper(3, 6, 3, 6)
    genboxConstraintsHelper(3, 6, 6, 9)
    genboxConstraintsHelper(6, 9, 0, 3)
    genboxConstraintsHelper(6, 9, 3, 6)
    genboxConstraintsHelper(6, 9, 6, 9)


def loadSudoku(board):
    """
    Load a Sudoku board and return the variables, indexes, domains, assignments, and constraints.

    Parameters:
    - board (list): A 2D list representing the Sudoku board.

    Returns:
    - variables (list): A list of variable names.
    - indexes (dict): A dictionary mapping variable names to their indexes in the board.
    - domains (dict): A dictionary mapping variable names to their domains.
    - assignments (dict): A dictionary mapping variable names to their assigned values.
    - constraints (dict): A dictionary mapping variable names to their constraint lists.
    """
    variables = []
    indexes = {}
    domains = {}
    assignments = {}
    constraints = {}

    with open("map_constraints.txt", "r") as file:
        boxConstraints = [line.replace("\n", "") for line in file.readlines()]

    for i in range(0, len(board), 1):
        for j in range(0, len(board[i]), 1):
            name = f"{rowIndexKey[i]}{j+1}"
            value = board[i][j]
            domain = asvalue(standardDomain) if value == 0 else [value]
            constraintList = []

            if value != 0:
                constraintList.append(f"{name}=={value}")

            for row in range(len(board)):
                for col in range(len(board[row])):
                    if row == i and col != j:
                        constraintList.append(f"{name}!={rowIndexKey[row]}{col+1}")
                    if col == j and row != i:
                        constraintList.append(f"{name}!={rowIndexKey[row]}{col+1}")

            for constraint in boxConstraints:
                if name in constraint[:2]:
                    constraintList.append(constraint)

            variables.append(name)
            indexes[name] = [i, j]
            domains[name] = domain
            assignments[name] = value
            constraints[name] = constraintList

    return variables, indexes, domains, assignments, constraints


def evaluateConstraint(constraint: str, assignments: dict):
    """
    Evaluate a constraint based on the current variable assignments.

    Parameters:
    constraint (str): The constraint to evaluate.
    assignments (dict): A dictionary containing variable assignments.

    Returns:
    bool: True if the constraint is satisfied, False otherwise.
    """
    yKey: str = constraint[4:]
    if yKey.isnumeric():
        return assignments[constraint[0:2]] == int(yKey)
    return assignments[constraint[0:2]] != assignments[constraint[4:]]


def revise(variableName, domains, constraints, assignments):
    """
    Revises the domain of a variable based on the constraints and assignments.

    Args:
        variableName (str): The name of the variable to revise.
        domains (dict): A dictionary mapping variable names to their domains.
        constraints (dict): A dictionary mapping variable names to their constraints.
        assignments (dict): A dictionary mapping variable names to their assigned values.

    Returns:
        bool: True if the domain of the variable is revised, False otherwise.
    """
    variableDomain = asvalue(domains[variableName])
    variableConstraints = constraints[variableName]
    originalVariableValue = asvalue(assignments[variableName])
    revised = False
    for domainValue in variableDomain:
        assignments[variableName] = domainValue
        for constraint in variableConstraints:
            if evaluateConstraint(constraint, assignments) == False:
                if domainValue in domains[variableName]:
                    domains[variableName].remove(domainValue)
                revised = True

    assignments[variableName] = originalVariableValue
    assignments[variableName] = originalVariableValue
    return revised


def ac3Algorithm(variables, domains, assignments, constraints):
    """
    Implements the AC-3 algorithm to enforce arc consistency.

    Parameters:
    - variables: A list of variables.
    - domains: A dictionary mapping variables to their domains.
    - assignments: A dictionary mapping variables to their assigned values.
    - constraints: A list of constraints.

    Returns:
    - True if the AC-3 algorithm succeeds in enforcing arc consistency.
    - False if the AC-3 algorithm fails and a domain becomes empty.
    """
    for variable in variables:
        revise(variable, domains, constraints, assignments)
        if len(domains[variable]) == 0:
            return False
    return True


def isConsistent(variable, value, assignments, constraints):
    """
    Check if assigning a value to a variable is consistent with the current assignments and constraints.

    Args:
        variable (str): The variable to assign a value to.
        value: The value to assign to the variable.
        assignments (dict): The current assignments of variables.
        constraints (dict): The constraints between variables.

    Returns:
        bool: True if the assignment is consistent, False otherwise.
    """
    copyAssignments: dict = asvalue(assignments)
    copyAssignments[variable] = value
    for constraint in constraints[variable]:
        if evaluateConstraint(constraint, copyAssignments) == False:
            return False
    return True


def updateAssignments(variables, assignments, domains, constraints):
    """
    Update the assignments based on the current domains and constraints.

    Parameters:
    - variables (list): A list of variables.
    - assignments (dict): A dictionary representing the current assignments.
    - domains (dict): A dictionary representing the current domains for each variable.
    - constraints (list): A list of constraints.

    Returns:
    - None
    """
    for variable in variables:
        if len(domains[variable]) == 1:
            if isConsistent(variable, domains[variable][0], assignments, constraints):
                assignments[variable] = domains[variable][0]
    return


def updateDomain(variables, assignments, domains):
    """
    Update the domains based on the current assignments.

    Parameters:
    - variables (list): A list of variables.
    - assignments (dict): A dictionary of variable assignments.
    - domains (dict): A dictionary of variable domains.

    Returns:
    None
    """
    for variable in variables:
        if assignments[variable] != 0:
            domains[variable] = [assignments[variable]]
    return


def updateConstraints(variables, assignments, constraints):
    """
    Update the constraints based on the current assignments.

    Parameters:
    - variables (list): A list of variables.
    - assignments (dict): A dictionary containing variable assignments.
    - constraints (dict): A dictionary containing constraints for each variable.

    Returns:
    - None

    This function updates the constraints dictionary based on the current assignments.
    For each variable in the variables list, if the variable has a non-zero assignment,
    it checks if the assignment is already present in the constraints dictionary.
    If not, it appends the assignment to the list of constraints for that variable.
    """
    for variable in variables:
        if assignments[variable] != 0:
            if f"{variable}=={assignments[variable]}" not in constraints[variable]:
                constraints[variable].append(f"{variable}=={assignments[variable]}")
    return


def updateAll(variables, domains, assignments, constraints):
    """
    Update the domains, assignments, and constraints based on the given variables.

    Parameters:
    variables (list): A list of variables.
    domains (dict): A dictionary mapping variables to their domains.
    assignments (dict): A dictionary mapping variables to their assigned values.
    constraints (list): A list of constraints.

    Returns:
    None
    """
    # Update the domains, assignments, and constraints
    updateDomain(variables, assignments, domains)
    updateAssignments(variables, assignments, domains, constraints)
    updateConstraints(variables, assignments, constraints)
    return


def isComplete(assignments):
    """
    Check if all variables have been assigned a value.

    Args:
        assignments (dict): A dictionary containing variable assignments.

    Returns:
        bool: True if all variables have been assigned a value, False otherwise.
    """
    for assignment in assignments:
        if assignments[assignment] == 0:
            return False
    return True


def selectUnassignedVariable(variables, domains):
    """
    Selects an unassigned variable with the fewest remaining values.

    Args:
        variables (list): A list of variables.
        domains (dict): A dictionary mapping variables to their domains.

    Returns:
        The variable with the fewest remaining values.
    """
    minimum = 9
    minRemainingVal = None
    for variable in variables:
        if len(domains[variable]) != 1 and len(domains[variable]) < minimum:
            minimum = len(domains[variable])
            minRemainingVal = variable
    return minRemainingVal


def infer(variables, domains, assignments, constraints):
    """
    Infers new assignments for variables based on the given domains, assignments, and constraints.

    Args:
        variables (list): A list of variables.
        domains (dict): A dictionary mapping variables to their corresponding domains.
        assignments (dict): A dictionary mapping variables to their current assignments.
        constraints (list): A list of constraints.

    Returns:
        tuple: A tuple containing the inferred assignments, updated domains, updated constraints,
               and updated assignments if the AC3 algorithm is successful. Otherwise, it returns
               a tuple of False values.
    """
    copyVars = asvalue(variables)
    copyDomains = asvalue(domains)
    copyAssignments = asvalue(assignments)
    copyConstraints = asvalue(constraints)

    updateAll(copyVars, copyDomains, copyAssignments, copyConstraints)

    if ac3Algorithm(copyVars, copyDomains, copyAssignments, copyConstraints):
        updateAll(copyVars, copyDomains, copyAssignments, copyConstraints)
        inferences = {}
        for variable in variables:
            if assignments[variable] != copyAssignments[variable]:
                inferences[variable] = copyAssignments[variable]

        return inferences, copyDomains, copyConstraints, copyAssignments
    return (
        False,
        False,
        False,
        False,
    )


def backtrack(variables, domains, assignments, constraints):
    """
    Backtracking algorithm to solve the Sudoku puzzle.

    Args:
        variables (list): List of variables in the puzzle.
        domains (dict): Dictionary mapping variables to their domains.
        assignments (dict): Dictionary mapping variables to their assigned values.
        constraints (list): List of constraints for the puzzle.

    Returns:
        tuple: A tuple containing the updated domains, assignments, and constraints if a solution is found.
               If no solution is found, it returns False for all three elements.
    """
    if isComplete(assignments):
        return domains, assignments, constraints
    variable = selectUnassignedVariable(variables, domains)
    valueOriginal = asvalue(assignments[variable])

    for value in domains[variable]:
        if isConsistent(variable, value, assignments, constraints):
            assignments[variable] = value
            inferences, copyDomains, copyConstraints, copyAssignments = infer(
                variables, domains, assignments, constraints
            )

            if inferences != False:
                copyDomains, copyAssignments, copyConstraints = backtrack(
                    variables, copyDomains, copyAssignments, copyConstraints
                )
                if copyDomains != False:
                    return copyDomains, copyAssignments, copyConstraints
        assignments[variable] = valueOriginal

    return False, False, False


def solveSudoku(board):
    """
    Solves a Sudoku puzzle using the AC-3 algorithm and backtracking.

    Args:
        board (list): The Sudoku board represented as a 2D list.

    Returns:
        list: The solved Sudoku board as a 2D list. If the puzzle is unsolvable, an empty list is returned.
    """

    newBoard = []

    variables, indexes, domains, assignments, constraints = loadSudoku(board)
    if ac3Algorithm(variables, domains, assignments, constraints):
        updateAll(variables, domains, assignments, constraints)

        solved = True
        for variable in variables:
            solved = False if assignments[variable] == 0 else solved

        if solved == False:
            backTrackDomain, backTrackAsgn, backtracked_constraints = backtrack(
                variables, domains, assignments, constraints
            )

            if backTrackDomain != False:
                newBoard = assignToBoard(variables, backTrackAsgn)

            else:
                return newBoard

        else:
            newBoard = assignToBoard(variables, assignments)

    else:
        return newBoard
    return newBoard


if __name__ == "__main__":
    # Example Sudoku board
    board = [
        [0, 0, 3, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 8],
        [1, 0, 5, 2, 0, 8, 0, 6, 0],
        [0, 0, 0, 0, 1, 2, 3, 0, 5],
        [7, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 0, 1, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0],
        [3, 7, 0, 1, 0, 0, 0, 0, 2],
        [0, 0, 9, 0, 0, 0, 7, 5, 6],
    ]
    print("Initial Board")
    print(np.array(board))
    newBoard = solveSudoku(board)
    print("Solved board")
    print(np.array(newBoard))
