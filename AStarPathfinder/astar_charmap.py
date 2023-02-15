from queue import PriorityQueue


class Node:
    def __init__(self, pos, tot_rows):
        self.pos = pos
        self.state = 'base'
        self.neighbours = []
        self.tot_rows = tot_rows

    def get_pos(self):
        return self.pos

    def reset(self):
        self.state = 'base'

    def make_open(self):
        self.state == 'open'

    def make_start(self):
        self.state = 'start'

    def make_barrier(self):
        self.state = 'barrier'

    def is_barrier(self):
        return self.state == 'barrier'

    def make_destination(self):
        self.state = 'destination'

    def make_closed(self):
        self.state = 'closed'

    def make_path(self):
        self.state = 'path'

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.pos[0] > 0 and not grid[self.pos[0] - 1][self.pos[1]].is_barrier():  # UP
            self.neighbours.append(grid[self.pos[0] - 1][self.pos[1]])
        if self.pos[0] < self.tot_rows - 1 and not grid[self.pos[0] + 1][self.pos[1]].is_barrier():  # DOWN
            self.neighbours.append(grid[self.pos[0] + 1][self.pos[1]])
        if self.pos[0] > 0 and not grid[self.pos[0]][self.pos[1] - 1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.pos[0]][self.pos[1] - 1])
        if self.pos[1] < self.tot_rows - 1 and not grid[self.pos[0]][self.pos[1] + 1].is_barrier():  # RIGHT
            self.neighbours.append(grid[self.pos[0]][self.pos[1] + 1])


def map_to_array(map):
    map_arr = []
    for row in map:
        map_arr.append(['/', *row, '/'])
    return map_arr


def make_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(Node((i, j), rows))
    return grid


def get_SDB_pos(mat):
    start, destination, barriers = None, None, []
    for i, row in enumerate(mat):
        for j, node in enumerate(row):
            if node == 'S':
                start = (i, j)
            if node == 'D':
                destination = (i, j)
            if node == '/':
                barriers.append((i, j))
    return start, destination, barriers


def H(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def astar_algorithm(start, dest, grid):
    c, came_from, open_set = 0, {}, PriorityQueue()
    open_set.put((0, c, start))
    g_score = {node: float('inf') for row in grid for node in row}  # all → ♾️
    f_score = {node: float('inf') for row in grid for node in row}  # all → ♾️
    g_score[start] = 0
    f_score[start] = H(start.get_pos(), dest.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        curr = open_set.get()[2]
        open_set_hash.remove(curr)
        if curr == dest:
            rec_path(came_from, dest)
            start.make_start()
            return True

        for neighbor in curr.neighbours:
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = curr
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + H(neighbor.get_pos(), dest.get_pos())
                if neighbor not in open_set_hash:
                    c += 1
                    open_set.put((f_score[neighbor], c, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        if curr != start:
            curr.make_closed()
    return False


def rec_path(came_from, curr):
    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()


def display_path(map_arr, grid):
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            if node.state == 'path':
                map_arr[i][j] = '*'
    for c, row in enumerate(map_arr):
        map_arr[c] = ''.join(row)
    print(f'\nShortest Path from S → D:\n', *map_arr, sep='\n')


def read_map(map_path):
    with open(map_path, 'r') as mf:
        return [line.strip('\n').strip("'") for line in mf]


def main(map_ver):
    map_arr = map_to_array(read_map(f'CharMaps/map{str(map_ver)}.txt'))
    rows, cols = len(map_arr), len(map_arr[0])
    grid = make_grid(rows, cols)
    start_pos, destination_pos, barrier_pos = get_SDB_pos(map_arr)
    for row in grid:
        for node in row:
            if node.pos == start_pos:
                start = node
                node.make_start()
            elif node.pos == destination_pos:
                dest = node
                node.make_destination()
            elif any(node.pos == pos for pos in barrier_pos):
                node.make_barrier()
    for row in grid:
        for node in row:
            node.update_neighbours(grid)
    astar_algorithm(start, dest, grid)  # Start A* Algorithm
    display_path(map_arr, grid)


if __name__ == '__main__':
        # main(input('\n === Enter Map Version: '))
        main(1)
