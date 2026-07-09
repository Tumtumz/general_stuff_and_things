import pygame
import random

white  = (255, 255, 255)
black  = (  0,   0,   0)
grey   = (128, 128, 128)
red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
cyan   = (  0, 255, 255)
pink   = (255,   0, 255)
yellow = (255, 255,   0)

TILE_SIZE = 10

class EdgeThing:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False

class LineThing:
    def __init__(self, i, v1, v2):
        self.i = i
        self.v1 = v1
        self.v2 = v2
    
    def __repr__(self):
        return f"line_object(i = {self.i}, v1 = {self.v1}, v2 = {self.v2})"
    
    def __lt__(self, other):
        return self.i < other
    
    def __gt__(self, other):
        return self.i > other
    
    def __eq__(self, other):
        return self.i == other
    
    def __le__(self, other):
        return self.i <= other
    
    def	__ge__ (self, other):
        return self.i >= other

grid = []
edgemap = []
for x in range(int(1600 / TILE_SIZE)):
    grid.append([])
    edgemap.append([])
    for y in range(int(900 / TILE_SIZE)):
        grid[-1].append(False)
        edgemap[-1].append(EdgeThing())

pointer_x = 100.0
pointer_y = 100.0

toplines = []
bottomlines = []
leftlines = []
rightlines = []
TLlines = []
TRlines = []
BLlines = []
BRlines = []

def draw_grid():
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell:
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(window, grey, rect)

def draw_edgemap():
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell:
                if edgemap[x][y].up:
                    uprect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE / 5)
                    pygame.draw.rect(window, red, uprect)
                if edgemap[x][y].down:
                    downrect = (x * TILE_SIZE, y * TILE_SIZE + (TILE_SIZE * 4 / 5), TILE_SIZE, TILE_SIZE / 5)
                    pygame.draw.rect(window, red, downrect)
                if edgemap[x][y].left:
                    leftrect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE / 5, TILE_SIZE)
                    pygame.draw.rect(window, red, leftrect)
                if edgemap[x][y].right:
                    rightrect = (x * TILE_SIZE + (TILE_SIZE * 4 / 5), y * TILE_SIZE, TILE_SIZE / 5, TILE_SIZE)
                    pygame.draw.rect(window, red, rightrect)

def scan_edges():
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell:
                if x > 0:
                    edgemap[x][y].left = not grid[x-1][y] if x-1 >= 0 else False
                if x < int(1600 / TILE_SIZE):
                    edgemap[x][y].right = not grid[x+1][y] if x+1 < len(grid) else False
                if y > 0:
                    edgemap[x][y].up = not grid[x][y-1] if y-1 >= 0 else False
                if y < int(900 / TILE_SIZE):
                    edgemap[x][y].down = not grid[x][y+1] if y+1 < len(grid[x]) else False
            else:
                edgemap[x][y] = EdgeThing()

def make_lines():
    toplines.clear()
    bottomlines.clear()
    leftlines.clear()
    rightlines.clear()
    TLlines.clear()
    TRlines.clear()
    BLlines.clear()
    BRlines.clear()
    #4 passes, scan for vertical lines, then horizontal, then each diagonal
    #vertical scan first
    left_edge = None
    right_edge = None
    for x, row in enumerate(edgemap):
        for y, cell in enumerate(row):
            if cell.left and (not (cell.up or cell.down) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                #if we've found a cell with a left edge, it either is the top of the edge or it extends the same line as the cell above
                if not left_edge:
                    left_edge = LineThing(x, y, y+1)
                else:
                    left_edge.v2 = y+1
            elif left_edge:
                #if we've found a cell without a left edge and the cell above had one, that must have been the end of that edge
                leftlines.append(left_edge)
                left_edge = None
            if cell.right and (not (cell.up or cell.down) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                #ditto on right side
                if not right_edge:
                    right_edge = LineThing(x+1, y, y+1)
                else:
                    right_edge.v2 = y+1
            elif right_edge:
                rightlines.append(right_edge)
                right_edge = None
        #make sure when you reach the end of the scan you don't carry a line onto the next iteration
        if left_edge:
            leftlines.append(left_edge)
            left_edge = None
        if right_edge:
            rightlines.append(right_edge)
            right_edge = None
    #horizontal scan
    top_edge = None
    bottom_edge = None
    for y in range(len(edgemap[0])):
        for x, row in enumerate(edgemap):
            cell = row[y]
            if cell.up and (not (cell.left or cell.right) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                #if we've found a cell with a top edge, it either is the left end of the edge or it extends the same line as the cell to the left
                if not top_edge:
                    top_edge = LineThing(y, x, x+1)
                else:
                    top_edge.v2 = x+1
            elif top_edge:
                #if we've found a cell without a top edge and the cell to the left had one, that must have been the end of that edge
                toplines.append(top_edge)
                top_edge = None
            if cell.down and ( not (cell.left or cell.right) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                #ditto downwards
                if not bottom_edge:
                    bottom_edge = LineThing(y+1, x, x+1)
                else:
                    bottom_edge.v2 = x+1
            elif bottom_edge:
                bottomlines.append(bottom_edge)
                bottom_edge = None
        if top_edge:
            toplines.append(top_edge)
            top_edge = None
        if bottom_edge:
            bottomlines.append(bottom_edge)
            bottom_edge = None
    #now the fun begins with the diagonal scans...
    # / this way first /
    TL_edge = None
    BR_edge = None
    for x in range(len(edgemap) + len(edgemap[0])):
        for y in range(len(edgemap[0])):
            if x - y < 0 or x - y >= len(edgemap):
                continue
            cell = edgemap[x-y][y]
            if (cell.up and cell.left) and not (cell.down or cell.right):
                #if we've found a cell with a top left edge, it's either a new edge or it continues the line of the cell to the top right
                if not TL_edge:
                    TL_edge = LineThing(x+1, y, y+1)
                else:
                    TL_edge.v2 = y+1
            elif TL_edge:
                TLlines.append(TL_edge)
                TL_edge = None
            if (cell.down and cell.right) and not (cell.up or cell.left):
                if not BR_edge:
                    BR_edge = LineThing(x+1, y, y+1)
                else:
                    BR_edge.v2 = y+1
            elif BR_edge:
                BRlines.append(BR_edge)
                BR_edge = None
        if TL_edge:
                TLlines.append(TL_edge)
                TL_edge = None
        if BR_edge:
            BRlines.append(BR_edge)
            BR_edge = None
    # \ now this way \
    TR_edge = None
    BL_edge = None
    offset = len(edgemap[0])
    for x in range(len(edgemap) + len(edgemap[0])):
        for y in range(len(edgemap[0])):
            if x - offset + y < 0 or x - offset + y >= len(edgemap):
                continue
            cell = edgemap[x - offset + y][y]
            if cell.up and cell.right and not (cell.down or cell.left):
                if not TR_edge:
                    TR_edge = LineThing(x-offset, y, y+1)
                else:
                    TR_edge.v2 = y+1
            elif TR_edge:
                TRlines.append(TR_edge)
                TR_edge = None
            if cell.down and cell.left and not (cell.up or cell.right):
                if not BL_edge:
                    BL_edge = LineThing(x-offset, y, y+1)
                else:
                    BL_edge.v2 = y+1
            elif BL_edge:
                BLlines.append(BL_edge)
                BL_edge = None
        if TR_edge:
                TRlines.append(TR_edge)
                TR_edge = None
        if BL_edge:
                BLlines.append(BL_edge)
                BL_edge = None
    # rightlines.reverse()
    # bottomlines.reverse()
    # TRlines.reverse()
    # BRlines.reverse()

def draw_lines():
    for line in leftlines:
        pygame.draw.line(window, white, (line.i * TILE_SIZE, line.v1 * TILE_SIZE), (line.i * TILE_SIZE, (line.v2) * TILE_SIZE), 5)
    for line in rightlines:
        pygame.draw.line(window, white, ((line.i) * TILE_SIZE, line.v1 * TILE_SIZE), (line.i * TILE_SIZE, (line.v2) * TILE_SIZE), 5)
    for line in toplines:
        pygame.draw.line(window, white, (line.v1 * TILE_SIZE, line.i * TILE_SIZE), (line.v2 * TILE_SIZE, line.i * TILE_SIZE), 5)
    for line in bottomlines:
        pygame.draw.line(window, white, (line.v1 * TILE_SIZE, (line.i) * TILE_SIZE), (line.v2 * TILE_SIZE, line.i * TILE_SIZE), 5)
    for line in TRlines:
        pygame.draw.line(window, white, ((line.i + line.v1) * TILE_SIZE, line.v1 * TILE_SIZE), ((line.i + line.v2) * TILE_SIZE, (line.v2) * TILE_SIZE), 5)
    for line in BRlines:
        pygame.draw.line(window, white, ((line.i - line.v1) * TILE_SIZE, line.v1 * TILE_SIZE), ((line.i - line.v2) * TILE_SIZE, line.v2 * TILE_SIZE), 5)
    for line in BLlines:
        pygame.draw.line(window, white, ((line.i + line.v1) * TILE_SIZE, line.v1 * TILE_SIZE), ((line.i + line.v2) * TILE_SIZE, (line.v2) * TILE_SIZE), 5)
    for line in TLlines:
        pygame.draw.line(window, white, ((line.i - line.v1) * TILE_SIZE, line.v1 * TILE_SIZE), ((line.i - line.v2) * TILE_SIZE, line.v2 * TILE_SIZE), 5)

def draw_pointer():
    pygame.draw.circle(window, green, (pointer_x, pointer_y), 20)
    mouse = pygame.mouse.get_pos()
    pygame.draw.line(window, green, (pointer_x, pointer_y), mouse)
    x = pointer_x/TILE_SIZE
    y = pointer_y/TILE_SIZE
    dx = (mouse[0] - pointer_x)/TILE_SIZE
    dy = (mouse[1] - pointer_y)/TILE_SIZE
    x2 = x + dx
    y2 = y + dy
    value = check_collision(x, y, dx, dy)
    intersections = []
    while value:
        cx, cy, x2, y2 = value
        intersections.append((cx * TILE_SIZE, cy * TILE_SIZE))
        dx = x2 - cx
        dy = y2 - cy
        value = check_collision(cx, cy, dx, dy)
    intersections.append((x2 * TILE_SIZE, y2 * TILE_SIZE))
    for x, point in enumerate(intersections[:-1]):
        pygame.draw.circle(window, pink, point, 5)
        pygame.draw.line(window, blue, point, intersections[x+1], 2)
    pygame.draw.circle(window, cyan, intersections[-1], 10)

def first_greater(arr, target):
    if not arr:
        return 0
    if arr[0] > target:
        return 0
    if arr[-1] <= target:
        return len(arr)
    left = 0
    right = len(arr) - 1
    result = len(arr)
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] > target:
            result = mid 
            right = mid - 1
        else:
            left = mid + 1
    return result

def last_smaller(arr, target):
    if not arr:
        return -1
    if arr[-1] < target:
        return len(arr) - 1
    if arr[0] >= target:
        return - 1
    left = 0
    right = len(arr) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] < target:
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    return result

def check_collision(x, y, dx, dy):
    vertical = False
    horizontal = False
    if dx != 0 and dy != 0:
        slope = dy/dx
        c = y - slope * x
    elif dx == 0:
        vertical = True
        slope = None
    else:
        assert(dy == 0)
        horizontal = True
        slope = 0
        c = y
    intersection = False
    cx = 0
    cy = 0
    direction = None
    if dx > 0:
        index = first_greater(leftlines, x)
        end = last_smaller(leftlines, x + dx)
        lines = leftlines
        step = 1
    elif dx < 0:
        index = last_smaller(rightlines, x)
        end = first_greater(rightlines, x + dx)
        lines = rightlines
        step = -1
    else:
        step = 0
        index = 0
        end = 0
    while index != end + step:
        line = lines[index]
        if horizontal:
            yval = y
        else:
            yval = line.i * slope + c
        if line.v1 <= yval <= line.v2:
            intersection = True
            cx = line.i
            cy = yval
            direction = "left/right"
            break
        index += step
    if dy > 0:
        index = first_greater(toplines, y)
        if intersection:
            end = last_smaller(toplines, cy)
        else:
            end = last_smaller(toplines, y + dy)
        lines = toplines
        step = 1
    elif dy < 0:
        index = last_smaller(bottomlines, y)
        if intersection:
            end = first_greater(bottomlines, cy)
        else:
            end = first_greater(bottomlines, y + dy)
        lines = bottomlines
        step = -1
    else:
        step = 0
        index = 0
        end = 0
    while index != end + step:
        line = lines[index]
        if vertical:
            xval = x
        else:
            xval = (line.i - c) / slope
        if line.v1 <= xval <= line.v2:
            if not intersection or (step == 1 and cy > line.i) or (step == -1 and cy < line.i):
                intersection = True
                cx = xval
                cy = line.i
                direction = "up/down"
            break
        index += step
    # now we check against the diagonals...
    if dy < dx:
        index = first_greater(BLlines, (x - y))
        if intersection:
            end = last_smaller(BLlines, (cx - cy))
        else:
            end = last_smaller(BLlines, ((x + dx) - (y + dy)))
        lines = BLlines
        step = 1
    elif dy > dx:
        index = last_smaller(TRlines, (x - y))
        if intersection:
            end = first_greater(TRlines, (cx - cy))
        else:
            end = first_greater(TRlines, ((x + dx) - (y + dy)))
        lines = TRlines
        step = -1
    else:
        step = 0
        index = 0
        end = 0
    while index != end + step:
        line = lines[index]
        if vertical:
            xval = x
        elif slope == 1:
            xval = (line.i + c) / 2
        else:
            xval = (-line.i - c) / (slope - 1)
        yval = xval - line.i 
        if line.v1 <= yval <= line.v2:
            if not intersection or (step == 1 and cx - cy > xval - yval) or (step == -1 and cx - cy < xval - yval):
                intersection = True
                cx = xval
                cy = yval
                direction = "\\this way\\"
            break
        index += step
    if dy > -dx:
        index = first_greater(TLlines, (x + y))
        if intersection:
            end = last_smaller(TLlines, (cx + cy))
        else:
            end = last_smaller(TLlines, ((x + dx) + (y + dy)))
        lines = TLlines
        step = 1
    elif dy < -dx:
        index = last_smaller(BRlines, (x + y))
        if intersection:
            end = first_greater(BRlines, (cx + cy))
        else:
            end = first_greater(BRlines, ((x + dx) + (y + dy)))
        lines = BRlines
        step = -1
    else:
        step = 0
        index = 0
        end = 0
    while index != end + step:
        line = lines[index]
        if vertical:
            xval = x
        elif slope == -1:
            xval = (line.i - c) / 2
        else:
            xval = (line.i - c) / (slope + 1)
        yval = line.i - xval 
        if line.v1 <= yval <= line.v2:
            if not intersection or (step == 1 and cx + cy > xval + yval) or (step == -1 and cx + cy < xval + yval):
                intersection = True
                cx = xval
                cy = yval
                direction = "/this way/"
            break
        index += step
    if intersection:
        if direction == "up/down":
            x2 = x + dx
            y2 = cy - ((y+dy) - cy)
        elif direction == "left/right":
            x2 = cx - ((x+dx) - cx)
            y2 = y + dy
        elif direction == "/this way/":
            x2 = cx + cy - (y+dy)
            y2 = cy + cx - (x+dx)
        else:
            assert(direction == "\\this way\\")
            x2 = cx - cy + (y+dy)
            y2 = cy - cx + (x+dx)
        return cx, cy, x2, y2
    else:
        return False

def print_everything():
    print(f"x : {pointer_x/TILE_SIZE}")
    print(f"y : {pointer_y/TILE_SIZE}")
    mouse = pygame.mouse.get_pos()
    print(f"dx : {(mouse[0] - pointer_x)/TILE_SIZE}")
    print(f"dy : {(mouse[1] - pointer_y)/TILE_SIZE}")
    print("Top lines: ")
    print(toplines)
    print("Bottom lines: ")
    print(bottomlines)
    print("Left lines: ")
    print(leftlines)
    print("Right lines: ")
    print(rightlines)
    print("TL lines: ")
    print(TLlines)
    print("BR lines: ")
    print(BRlines)
    print("TR lines: ")
    print(TRlines)
    print("BL lines: ")
    print(BLlines)
    print("check_collision result:")
    print(check_collision(pointer_x/TILE_SIZE, pointer_y/TILE_SIZE, (mouse[0] - pointer_x)/TILE_SIZE, (mouse[1] - pointer_y)/TILE_SIZE))

pygame.init()
window = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
pygame.display.set_caption("edge_finder_tester")
while True:
    window.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_q:
                print_everything()
    if pygame.key.get_pressed()[pygame.K_f]:
        pointer_y -= 1
    if pygame.key.get_pressed()[pygame.K_w]:
        pointer_y -= 1
    if pygame.key.get_pressed()[pygame.K_s]:
        pointer_y += 1
    if pygame.key.get_pressed()[pygame.K_r]:
        pointer_x -= 1
    if pygame.key.get_pressed()[pygame.K_t]:
        pointer_x += 1
    if pygame.key.get_pressed()[pygame.K_a]:
        pointer_x -= 1
    if pygame.key.get_pressed()[pygame.K_d]:
        pointer_x += 1
    buttons = pygame.mouse.get_pressed(3)
    pos = pygame.mouse.get_pos()
    if buttons[0]:
        grid[int(pos[0]/TILE_SIZE)][int(pos[1]/TILE_SIZE)] = True
        scan_edges()
        make_lines()
    elif buttons[2]:
        grid[int(pos[0]/TILE_SIZE)][int(pos[1]/TILE_SIZE)] = False
        scan_edges()
        make_lines()
    draw_grid()
    draw_edgemap()
    draw_lines()
    draw_pointer()
    pygame.display.update()