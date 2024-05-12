import pygame

from main import solveSudoku

sub = 500 / 9

grid = [
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
emptyGrid = [
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


def validMove(matrix, col, row, val):
    """
    Check if a move is valid in a Sudoku matrix.

    Args:
            matrix (list): The Sudoku matrix.
            col (int): The column index of the move.
            row (int): The row index of the move.
            val (int): The value of the move.

    Returns:
            bool: True if the move is valid, False otherwise.
    """
    for i in range(9):
        if matrix[col][i] == val:
            return False
        if matrix[i][row] == val:
            return False
    a = col // 3
    b = row // 3
    for x in range(a * 3, a * 3 + 3):
        for y in range(b * 3, b * 3 + 3):
            if matrix[x][y] == val:
                return False
    return True


pygame.font.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("sudokuSolveAI")

val = 0

x = 0
y = 0

fontOne = pygame.font.SysFont("Times New Roman", 30, "bold")
fontTwo = pygame.font.SysFont("Times New Roman", 26, "bold")


def getCoord(pos):
    """
    Returns the coordinates of a given position on the GUI grid.

    Parameters:
    pos (tuple): The position on the GUI grid.

    Returns:
    tuple: The coordinates (x, y) of the position on the grid.
    """
    global x
    x = pos[0] // sub
    global y
    y = pos[1] // sub


def drawBox():
    """
    Draws a box on the screen using pygame.

    This function draws a box on the screen using the pygame library. The box is drawn with two horizontal lines and two vertical lines, forming a rectangular shape.

    Parameters:
    None

    Returns:
    None
    """
    for i in range(2):
        pygame.draw.line(
            screen,
            (6, 44, 67),
            (x * sub - 3, (y + i) * sub),
            (x * sub + sub + 3, (y + i) * sub),
            7,
        )
        pygame.draw.line(
            screen,
            (6, 44, 67),
            ((x + i) * sub, y * sub),
            ((x + i) * sub, y * sub + sub),
            7,
        )


def draw():
    """
    Draws the Sudoku grid on the screen.

    This function iterates over the Sudoku grid and draws the filled cells as rectangles
    with the corresponding number inside. It also draws the grid lines to separate the cells.

    Parameters:
    None

    Returns:
    None
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(
                    screen, (85, 145, 169), (i * sub, j * sub, sub + 1, sub + 1)
                )

                textOne = fontOne.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(textOne, (i * sub + 20, j * sub + 11))
    for i in range(10):
        if i % 3 == 0:
            thick = 5
            colourbold = 1.20
        else:
            thick = 2
            colourbold = 0
        pygame.draw.line(
            screen, (6, 44 * colourbold, 67), (0, i * sub), (500, i * sub), thick
        )
        pygame.draw.line(
            screen, (6, 44 * colourbold, 67), (i * sub, 0), (i * sub, 500), thick
        )


def drawValue(val):
    textOne = fontOne.render(str(val), 1, (0, 0, 0))
    screen.blit(textOne, (x * sub + 15, y * sub + 15))


run = True
stateOne = 0
stateTwo = 0

while run:

    screen.fill((206, 205, 224))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            stateOne = 1
            pos = pygame.mouse.get_pos()
            getCoord(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                stateOne = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                stateOne = 1
            if event.key == pygame.K_UP:
                y -= 1
                stateOne = 1
            if event.key == pygame.K_DOWN:
                y += 1
                stateOne = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                stateTwo = 1
            if event.key == pygame.K_a:

                stateTwo = 0
                grid = [
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
            if event.key == pygame.K_d:
                stateTwo = 0
                grid = [
                    [0, 0, 1, 0, 7, 0, 0, 3, 0],
                    [0, 0, 0, 0, 0, 0, 0, 7, 0],
                    [3, 0, 5, 0, 0, 0, 2, 0, 9],
                    [0, 0, 2, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [6, 0, 8, 2, 0, 5, 0, 0, 0],
                    [0, 2, 0, 3, 0, 0, 0, 0, 7],
                    [0, 0, 6, 0, 0, 1, 0, 0, 5],
                    [0, 8, 0, 5, 0, 0, 0, 2, 6],
                ]
            if event.key == pygame.K_s:
                if grid != emptyGrid:

                    stateTwo = 0
                    grid = solveSudoku(grid)

    if val != 0:
        drawValue(val)
        if validMove(grid, int(x), int(y), val) == True:
            grid[int(x)][int(y)] = val
            stateOne = 0
        else:
            grid[int(x)][int(y)] = 0
        val = 0

    draw()
    if stateOne == 1:
        drawBox()

    pygame.display.update()

pygame.quit()
