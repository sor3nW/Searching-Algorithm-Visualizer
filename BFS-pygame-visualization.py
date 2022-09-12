import collections
import random
import pygame
from pygame.locals import *
from collections import deque
pygame.init()
pygame.font.init()

dimensions = screenWidth, screenHeight = 500,800
screen = pygame.display.set_mode((dimensions))
# this is the first commit from github
# now Im making a change from my local repository
# making sure this works
# making sure this works again
num = 15
grid = [[0 for i in range(num)]for j in range(num)]
diff = screenWidth//num
font1 = pygame.font.SysFont("menlo", 20)

def get_cord(pos):
    global x
    x = pos[0] // diff
    global y
    y = pos[1] // diff
def printGrid():
    for i in range(num):
        print(grid[i])
drawPoint = False
def draw():
    for i in range(num ):
        pygame.draw.line(screen, (0,0,0), (i * diff, 0), (i * diff, screenWidth -3))
        pygame.draw.line(screen, (0,0,0), (0, i * diff + diff), (screenWidth, i * diff + diff))

        for j in range(num):
            if grid[i][j] == 1:
                pygame.draw.rect(screen, (0,0,0), ((i * diff)+1,(j * diff)+1 ,diff, diff-1))
            if grid[i][j] == 2:
                pygame.draw.rect(screen, (150,150,255), ((i * diff)+1,(j * diff)+1 ,diff, diff-1))

            if grid[i][j] == 10 and drawPoint == True:
                pygame.draw.rect(screen, (0,0,0), ((i * diff)+1,(j * diff)+1 ,diff, diff-1))
def clear_board():
    for i in range(num):
        for j in range(num):
            grid[i][j] = 0



def breadthFirst(r, c):
    visit = set()
    q = collections.deque()
    print((r, c))
    visit.add((r, c))
    q.append((r, c))

    run = True
    while q:

        if run == True:
            row, col = q.popleft()
            directions = [[1,0],[-1,0],[0,1],[0,-1]]
            for r, c in directions:
                r, c = row + r, col + c
                if r in range(len(grid)) and c in range(len(grid[0])) and (r, c) not in visit and grid[r][c] == 0:
                    visit.add((r, c))
                    q.append((r, c))
                    grid[r][c] = 2
                if r in range(len(grid)) and c in range(len(grid[0])) and (r, c) not in visit and grid[r][c] == 10:

                    return (r, c)



def secondPoint():

    pointx, pointy = random.randint(0, num-1), random.randint(0,num-1)
    if grid[pointx][pointy] == 1:
        secondPoint()
    else:
        return pointx, pointy








firstCoord = 0,0
secondCoord = 0,0
chosen = 0
flag1 = 0
flag2 = 0
coordText1 = None
coordText2 = None
run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_r:
                clear_board()
                chosen = 0
                flag2 = 0
                drawPoint = False
            if event.key == pygame.K_RETURN and chosen == 2:
                drawPoint = True
                chosen = 3
                gridrun = True
                flag2 = 1
                for i in range(len(grid)):
                    for j in range(len(grid[0])):

                        if gridrun:
                            if grid[i][j] == 1 and (i, j):
                                coordText2 = breadthFirst(i, j)
                                coordText1 = (i, j)
                                gridrun = False
                                print(coordText2)
                                print(coordText1)





        if event.type == pygame.MOUSEBUTTONDOWN and chosen < 2:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
            if chosen == 0:
                firstCoord = x, y
                secondCoord = secondPoint()




    if flag1 == 1:
        grid[x][y] = 1
        grid[secondCoord[0]][secondCoord[1]] = 10
        chosen += 2
        flag1 = 0




    screen.fill((255,255,255))
    draw()
    text1 = font1.render("the first coordinate:", False, (0,0,0))
    text2 = font1.render("the second coordinate:", False, (0,0,0))
    screen.blit(text1, (50, 550))
    screen.blit(text2, (50, 650))

    if flag2 == 1:
        coord1 = font1.render(f"{coordText1} ", False, (0, 0, 0))
        coord2 = font1.render(f"{coordText2}", False, (0, 0, 0))
        screen.blit(coord1, (300, 550))
        screen.blit(coord2, (310, 650))
    #WHEN YOU UPDATE THIS PROGRAM MAKE IT SO THAT HTHE PROGRAM DOESNT KNOW WHAT THE SECOND POINT IS AND HAS TO FIND IT
    #THEN AFTER IT FINDS THE POINT IT RUNS DIJKSTRAS ALGORITHM TO FIND THE SHORTEST PATH

    #ALSO NEW IDEA. WRITE FLASHCARD APP THAT MAKES YOU SAY THE ANSWER

    pygame.display.update()
pygame.quit()
