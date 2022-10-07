
import pygame

from queue import PriorityQueue
from collections import deque

dim = screen_W, screen_H = 500,700
screen = pygame.display.set_mode((dim))
num = 25
div = screen_W // num

colors = {
    "black": (0,0,0),
    "white": (255,255,255),
    "green": (100,255,100),
    "red": (255,100,100),
    "purple": (150,150,255),
    "grey": (150,150,150)
}


class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = colors["white"]
        self.rect = pygame.draw.rect(screen, self.color, pygame.Rect(row*div+5, col*div+5, div-10, div-10))
        self.neighbors = []

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.row * div +1, self.col * div +1, div - 1, div - 1))

    def iswall(self):
        return self.color == colors["black"]

    def isnotwall(self):
        return self.color != colors["black"]

    

    def add_neighbors(self, grid):
        self.neighbors = []
        if (self.row + 1) in range(num) and grid[self.row+1][self.col].isnotwall():
            self.neighbors.append(grid[self.row+1][self.col])
        if (self.row - 1) in range(num) and grid[self.row-1][self.col].isnotwall():
            self.neighbors.append(grid[self.row-1][self.col])
        if (self.col + 1) in range(num) and grid[self.row][self.col+1].isnotwall():
            self.neighbors.append(grid[self.row][self.col+1])
        if (self.col-1) in range(num) and grid[self.row][self.col-1].isnotwall():
            self.neighbors.append(grid[self.row-1][self.col-1])

def get_pos(r, c):
    x = r // div
    y = c // div
    return x, y

def draw(array):
    draw_boxes(array)
    for i in range(num):
        for j in range(num):

            pygame.draw.line(screen, colors["grey"], (i * div, 0), (i * div, screen_W) )
            pygame.draw.line(screen, colors["grey"], (0, i * div + div), (screen_W, i * div + div) )

def draw_boxes(grid):
    for row in grid:
        for box in row:
            box.draw()

def array():
    array = []
    for i in range(num):
        array.append([])
        for j in range(num):
            box = Box(i, j)
            array[i].append(box)
    return array




def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = colors["purple"]
        draw()


def heuristic(p1, p2):
    
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def aStarPathfind(grid, start, end, draw):
    count = 0
    openSet = PriorityQueue()
    cameFrom = {}

    gScore = {spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0

    fScore = {spot: float("inf") for row in grid for spot in row}
    
    fScore[start] = heuristic((start.row, start.col), (end.row, end.col))

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        if current == end:
            reconstruct_path(cameFrom, current, draw)

        for neighbor in current.neighbor:
            tentative_gScore = gScore[current] + 1
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + heuristic((neighbor.row, neighbor.col), (end.row, end.col))
                if neighbor not in openSet:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    neighbor.color = colors["green"]
        if current != start:
            current.color = colors["red"]
    return False

def breadthFirstSearch(x, y, grid, draw):
    
    
    q = deque()
    visit = set()
    q.append((x, y))
    visit.add((x, y))
    
    while q:
        i, j = q.popleft()
        grid[i][j].color = colors["red"]
        
        directions = [[1,0], [0,1], [-1,0], [0,-1]]
        for r, c in directions:
            nextRow, nextCol = i + r, j + c
            if ( nextRow in range(num) and nextCol in range(num) and grid[nextRow][nextCol].isnotwall() and (nextRow, nextCol) not in visit):
                q.append((nextRow, nextCol))
            if grid[nextRow][nextCol].color == colors["purple"] and (nextRow, nextCol) not in visit:
                grid[x][y].color = colors["purple"]
                return True
    return False


                


def main():
    start = None
    end = None
    let = "s"
    pointCount = 0
    grid = array()
    flag1 = False
    flag2 = False
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_r:
                    grid = array()
                    pointCount = 0
                if event.key == pygame.K_w:
                    let = "w"
                if event.key == pygame.K_s:
                    let = "s"
                if event.key == pygame.K_a:
                    let = "a"
                if event.key == pygame.K_b:
                    let = "b"

                if event.key == pygame.K_RETURN and pointCount == 2:
                    for r in grid:
                        for spot in r:
                            spot.add_neighbors(grid)
                    if let == "a":
                        aStarPathfind(grid, start, end, lambda: draw(grid))

                    if let == "b":
                        breadthFirstSearch(start.row, start.col, grid, lambda: draw(grid))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if let == "w":
                    flag1 = True
                if let == "s":
                    flag2 = True

            if event.type == pygame.MOUSEBUTTONUP:
                flag1 = False

        if flag1 == True:
            r, c = pygame.mouse.get_pos()
            x, y = get_pos(r, c)
            spot = grid[x][y]
            if let == "w":
                spot.color = colors["black"]

        if flag2 == True:
            if let == "s" and pointCount < 2:
                r, c = pygame.mouse.get_pos()
                x, y = get_pos(r, c)
                spot = grid[x][y]

                if pointCount == 0:
                    start = spot
                    
                if pointCount == 1:
                    end = spot
                spot.color = colors["purple"]
                pointCount += 1

                flag2 = False




        screen.fill((255,255,255))

        draw(grid)
        pygame.display.update()

    pygame.quit()
main()