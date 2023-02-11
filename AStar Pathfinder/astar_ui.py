import pygame
import math
from queue import PriorityQueue

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
premade_labyrinth_layout_path = 'assets/labyrinth.txt'
pygame.display.set_caption('A* Pathfinder Algorithm')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TEAL = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, tot_rows):
        self.row = row
        self.col = col
        self.x = width * row
        self.y = width * col
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.tot_rows = tot_rows

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = WHITE

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TEAL

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TEAL

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.row < self.tot_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

        if self.col < self.tot_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def H(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def rec_path(came_from, curr, draw):
    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()
        draw()


def astar_algorithm(draw, grid, start, end):
    cnt, open_set = 0, PriorityQueue()
    open_set.put((0, cnt, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}  # all -> ♾️
    f_score = {node: float('inf') for row in grid for node in row}  # all -> ♾️
    g_score[start] = 0
    f_score[start] = H(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        curr = open_set.get()[2]
        open_set_hash.remove(curr)

        if curr == end:
            rec_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in curr.neighbours:
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = curr
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + H(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    cnt += 1
                    open_set.put((f_score[neighbor], cnt, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if curr != start:
            curr.make_closed()
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def read_grid_layout(path):
    with open(path, 'r') as f:
        return [line.strip('\n') for line in f]


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS, start, end = 50, None, None
    grid = make_grid(ROWS, width)

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LMB
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if row >= 0 and row < ROWS and col >= 0 and col < ROWS:
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != start and node != end:
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RMB
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_x: # Clear Grid
                    start, end, grid = None, None, make_grid(ROWS, width)
                if event.key == pygame.K_l: # Load Labyrinth - MAYBE l + 1 etc.
                    print(read_grid_layout(premade_labyrinth_layout_path))
                    # start, end, grid = None, None, make_grid(ROWS, width)
    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH)
