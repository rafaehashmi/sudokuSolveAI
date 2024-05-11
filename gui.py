import pygame
from main import solve_sudoku
sub = 500 / 9

grid =[
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0]
	]
empty_grid =[
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0]
	]

def validMove(matrix, col, row, val):
    for i in range(9):
        if matrix[col][i]== val:
            return False
        if matrix[i][row]== val:
            return False
    a = col//3
    b = row//3
    for x in range(a * 3, a * 3 + 3):
        for y in range (b * 3, b * 3 + 3):
            if matrix[x][y]== val:
                return False
    return True

pygame.font.init()
screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption("Sudoku Solver with AC3 and Backtracking")

val = 0

x = 0
y = 0

font1 = pygame.font.SysFont("Times New Roman", 30, "bold")
font2 = pygame.font.SysFont("Times New Roman", 26, "bold")
def get_cord(pos):
	global x
	x = pos[0]//sub
	global y
	y = pos[1]//sub

def draw_box():
	for i in range(2):
		pygame.draw.line(screen, (6, 44, 67), (x * sub-3, (y + i)*sub), (x * sub + sub + 3, (y + i)*sub), 7)
		pygame.draw.line(screen, (6, 44, 67), ( (x + i)* sub, y * sub ), ((x + i) * sub, y * sub + sub), 7)

def draw():
		
	for i in range (9):
		for j in range (9):
			if grid[i][j]!= 0:

				pygame.draw.rect(screen, (85, 145, 169), (i * sub, j * sub, sub + 1, sub + 1))

				text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
				screen.blit(text1, (i * sub + 20, j * sub + 11))
	for i in range(10):
		if i % 3 == 0 :
			thick = 5
			colourbold = 1.20
		else:
			thick = 2
			colourbold = 0
		pygame.draw.line(screen, (6, 44 * colourbold, 67), (0, i * sub), (500, i * sub), thick)
		pygame.draw.line(screen, (6, 44 * colourbold, 67), (i * sub, 0), (i * sub, 500), thick)	

def draw_val(val):
	text1 = font1.render(str(val), 1, (0, 0, 0))
	screen.blit(text1, (x * sub + 15, y * sub + 15))




def instruction():
	text1 = font2.render("Press D to get a default configuration", 1, (0, 50, 0))
	text2 = font2.render("Press S to solve Sudoku", 1, (0, 50, 0))
	text3 = font2.render("Press A to clear screen", 1, (0, 50, 0))

	
	screen.blit(text1, (20, 520))	
	screen.blit(text2, (20, 620))
	screen.blit(text3, (20, 720))


run = True
state1 = 0
state2 = 0

while run:
	
	screen.fill((206, 205, 224))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			state1 = 1
			pos = pygame.mouse.get_pos()
			get_cord(pos)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x-= 1
				state1 = 1
			if event.key == pygame.K_RIGHT:
				x+= 1
				state1 = 1
			if event.key == pygame.K_UP:
				y-= 1
				state1 = 1
			if event.key == pygame.K_DOWN:
				y+= 1
				state1 = 1
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
				state2 = 1
			if event.key == pygame.K_a:

				state2 = 0
				grid =[
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0]
				]
			if event.key == pygame.K_d:
				state2 = 0
				grid =[
					[7, 8, 0, 4, 0, 0, 1, 2, 0],
					[6, 0, 0, 0, 7, 5, 0, 0, 9],
					[0, 0, 0, 6, 0, 1, 0, 7, 8],
					[0, 0, 7, 0, 4, 0, 2, 6, 0],
					[0, 0, 1, 0, 5, 0, 9, 3, 0],
					[9, 0, 4, 0, 6, 0, 0, 0, 5],
					[0, 7, 0, 3, 0, 0, 0, 1, 2],
					[1, 2, 0, 0, 0, 7, 4, 0, 0],
					[0, 4, 9, 2, 0, 6, 0, 0, 7]
				]
			if event.key == pygame.K_s:
				if grid != empty_grid:
	
					state2 = 0
					grid = solve_sudoku(grid)

	if val != 0:		
		draw_val(val)
		if validMove(grid, int(x), int(y), val)== True:
			grid[int(x)][int(y)]= val
			state1 = 0
		else:
			grid[int(x)][int(y)]= 0
		val = 0
	
	draw()
	if state1 == 1:
		draw_box()	
	instruction()

	pygame.display.update()

pygame.quit()	
	