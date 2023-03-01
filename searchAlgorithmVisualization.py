import random
from collections import deque
import pygame
from queue import PriorityQueue

screenWidth = 500
screen = pygame.display.set_mode((screenWidth,750))
num = 50
diff = screenWidth // num

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.maxRows = num
        self.neighbors = []
    def get_pos(self):
        return self.row, self.col

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.row * diff, self.col * diff, diff + 1, diff + 1))

    def isWall(self):
        return self.color == BLACK

    def make_neighbors(self, grid):
        self.neighbors = []
        if (self.row + 1 < self.maxRows and grid[self.row + 1][self.col].color != BLACK):
            self.neighbors.append(grid[self.row + 1][self.col])
        if (self.col + 1 < self.maxRows and grid[self.row][self.col + 1].color != BLACK):
            self.neighbors.append(grid[self.row][self.col + 1])
        if (self.row - 1 >= 0 and grid[self.row - 1][self.col].color != BLACK):
            self.neighbors.append(grid[self.row - 1][self.col])
        if (self.col - 1 >= 0 and grid[self.row][self.col - 1].color != BLACK):
            self.neighbors.append(grid[self.row][self.col - 1])




def drawLines():
    for i in range(num):
        pygame.draw.line(screen, GREY, (i * diff, 0), (i * diff, screenWidth))
        pygame.draw.line(screen, GREY, (0, i * diff + diff), (screenWidth, i * diff + diff))
def random_number():
    num1, num2 = random.randint(0, num-1), random.randint(0, num-1)
    if grid[num1][num2].color != WHITE:
        return random_number()
    else:
        return grid[num1][num2]
def fillrandom(grid):
    for row in grid:
        for box in row:
            number = random.randint(1,4)
            if number == 1:
                box.color = BLACK
    start = random_number()
    start.color = PURPLE
    end = random_number()
    end.color = PURPLE
    return start, end

def drawBoxes(grid):
    for row in grid:
        for box in row:
            box.draw()


def draw(grid):
    screen.fill(WHITE)
    drawBoxes(grid)
    drawLines()
    pygame.display.update()


def get_pos(x, y):
    newx = x // diff
    newy = y // diff
    return newx, newy

def depthfirst(x, y, grid, draw, start, end):

    q = deque()
    visit = set()
    q.append((x, y))
    visit.add((x, y))
    while q:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw()
        grid[x][y].color = PURPLE
        r, c = q.pop()
        grid[r][c].color = RED
        for neighbor in grid[r][c].neighbors:

            if (neighbor.color != BLACK and neighbor.color != PURPLE and (neighbor.row, neighbor.col) not in visit):
                q.append((neighbor.row, neighbor.col))
                visit.add((neighbor.row, neighbor.col))
                neighbor.color = GREEN

            if (neighbor.color == PURPLE and (neighbor.row, neighbor.col) not in visit):
                q.clear()
                copyastar(draw, grid, start, end)
                return True
    return False

def breadthFirst(x, y, grid, draw, start, end):

    q = deque()
    visit = set()
    q.append((x, y))
    visit.add((x, y))

    while q:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw()
        grid[x][y].color = PURPLE
        r, c = q.popleft()
        grid[r][c].color = RED
        for neighbor in grid[r][c].neighbors:

            if (neighbor.color != BLACK and neighbor.color != PURPLE and (neighbor.row, neighbor.col) not in visit):
                q.append((neighbor.row, neighbor.col))
                visit.add((neighbor.row, neighbor.col))
                neighbor.color = GREEN

            if (neighbor.color == PURPLE and (neighbor.row, neighbor.col) not in visit):
                q.clear()
                copyastar(draw, grid, start, end)
                return True
    return False


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = PURPLE
        draw()

def copyastar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {box: float("inf") for row in grid for box in row}
    g_score[start] = 0
    f_score = {box: float("inf") for row in grid for box in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)

            return True

        for neighbor in current.neighbors:

            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)





    return False

def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {box: float("inf") for row in grid for box in row}
    g_score[start] = 0
    f_score = {box: float("inf") for row in grid for box in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.color = PURPLE
            return True

        for neighbor in current.neighbors:

            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = GREEN

        draw()

        if current != start:
            current.color = RED
    return False


def gridAndNeighbors():
    grid = [[] for j in range(num)]
    for i in range(num):
        for j in range(num):
            box = Box(i, j)
            grid[i].append(box)

    return grid


grid = gridAndNeighbors()

start = None
end = None
randomcount = 0
flag1 = False
walls = False
let = None
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_r:
                start = None
                end = None
                let = None
                walls = False
                grid = gridAndNeighbors()
                randomcount = 0
            if event.key == pygame.K_i:
                let = "i"

            if event.key == pygame.K_w:
                walls = True

            if event.key == pygame.K_d:
                let = "d"

            if event.key == pygame.K_1 and randomcount < 1:
                i, j = fillrandom(grid)
                start = i
                end = j
                randomcount +=1
            if event.key == pygame.K_RETURN and start and end:
                if not let:
                    for row in grid:
                        for box in row:
                            box.make_neighbors(grid)
                    breadthFirst(start.row, start.col, grid, lambda: draw(grid), start, end)
                if let == "i":
                    for row in grid:
                        for box in row:
                            box.make_neighbors(grid)
                    astar(lambda: draw(grid), grid, start, end)
                if let == "d":
                    for row in grid:
                        for box in row:
                            box.make_neighbors(grid)
                    depthfirst(start.row, start.col, grid, lambda: draw(grid), start, end)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            r, c = get_pos(x, y)
            box = grid[r][c]
            if not start or not end:
                if not start:
                    start = box
                    box.color = PURPLE
                elif start and not end:
                    end = box
                    box.color = PURPLE
            if walls:
                flag1 = True
        if event.type == pygame.MOUSEBUTTONUP:
            flag1 = False
        if flag1:
            x, y = pygame.mouse.get_pos()
            r, c = get_pos(x, y)
            box = grid[r][c]
            box.color = BLACK

    draw(grid)

pygame.quit()
