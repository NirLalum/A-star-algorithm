import pygame
import math
from path_finder_algorithms import A_star_algo as algorithm

WITDH = 800 # the grid will be 800X800 pixels # clariffication: x is to the right and y is down
WIN = pygame.display.set_mode((WITDH,WITDH)) # creating the surface of the map
pygame.display.set_caption("Path Finding")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# create the class of the cubes
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width # width is the width of the spot not the grid
        self.y = row * width
        self.point = (self.x, self.y)
        self.color = WHITE # at first all white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        # will be updated later
        self.g = None
        self.f = None # f = g + h
        

    def get_pos(self):
        return self.row, self.col

    # check if node is in the closed list (allready visited)
    def is_closed(self):
        return self.color == RED

    # is the node in the fringe
    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) # win is the surface object from the beggining of the code

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return self.g < other.g


# define manheten huristic func
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# create the grid. cols number == rows number
def make_grid(rows, grid_width):
    grid = []
    gap = grid_width // rows # calc the width of each cube
    for i in range(rows):
        grid.append([]) # each row is a list
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

# draw grid lines (the grey lines) not the spots!
def draw_grid(win, rows, grid_width):
    gap = grid_width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (grid_width, i * gap)) # create the horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, grid_width)) # create the vecrtical lines 

# drawing the spots
def draw(win, grid, rows, width):
    win.fill(WHITE) # draw all spots to white

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, grid_width):
    gap = grid_width // rows
    x, y = pos

    row = y // gap
    col = x // gap

    return row, col

# this function will paint the path founded in purple
def reconstruct_path(draw, CLOSE,start, end):
    current = end
    while current != start:
        tmp_current = current
        for neighbor in current.neighbors:
            if neighbor.g != None and neighbor in CLOSE and neighbor.g < tmp_current.g:
                tmp_current = neighbor
        current = tmp_current
        if current != start:
            current.make_path()
        draw()

if __name__ == '__main__':
    def main(win, grid_width):
        ROWS = 50
        grid = make_grid(ROWS, grid_width)
        
        start = None # start node
        end = None # end node

        run = True
        started = False
        while run:
            draw(win, grid, ROWS, grid_width)
            for event in pygame.event.get(): # event is pressing a keyboard, mouse, etc...
                if event.type == pygame.QUIT:
                    run = False
                
                # make sure the if the algorithem has started the user wont be able to change anything in the board
                if started:
                    continue

                if pygame.mouse.get_pressed()[0]: # if left key was pressed
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, grid_width)
                    spot = grid[row][col] # access the spot that we clicked on
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                # reset the spot (make it white)
                elif pygame.mouse.get_pressed()[2]: # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, grid_width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

                # if the space key is pressed then start algo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        algorithm(lambda: draw(win, grid, ROWS, grid_width), h, reconstruct_path, grid, start, end)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = make_grid(ROWS, grid_width)

        pygame.QUIT

    main(WIN, WITDH)


