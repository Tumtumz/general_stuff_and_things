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
for x in range(int(1600 / 50)):
    grid.append([])
    edgemap.append([])
    for y in range(int(900 / 50)):
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
                rect = (x * 50, y * 50, 50, 50)
                pygame.draw.rect(window, grey, rect)

def draw_edgemap():
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell:
                if edgemap[x][y].up:
                    uprect = (x * 50, y * 50, 50, 10)
                    pygame.draw.rect(window, red, uprect)
                if edgemap[x][y].down:
                    downrect = (x * 50, y * 50 + 40, 50, 10)
                    pygame.draw.rect(window, red, downrect)
                if edgemap[x][y].left:
                    leftrect = (x * 50, y * 50, 10, 50)
                    pygame.draw.rect(window, red, leftrect)
                if edgemap[x][y].right:
                    rightrect = (x * 50 + 40, y * 50, 10, 50)
                    pygame.draw.rect(window, red, rightrect)

def scan_edges():
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell:
                if x > 0:
                    edgemap[x][y].left = not grid[x-1][y] if x-1 >= 0 else False
                if x < int(1600 / 50):
                    edgemap[x][y].right = not grid[x+1][y] if x+1 < len(grid) else False
                if y > 0:
                    edgemap[x][y].up = not grid[x][y-1] if y-1 >= 0 else False
                if y < int(900 / 50):
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
                    left_edge = LineThing(x, y, y)
                else:
                    left_edge.v2 = y
            elif left_edge:
                #if we've found a cell without a left edge and the cell above had one, that must have been the end of that edge
                leftlines.append(left_edge)
                left_edge = None
            if cell.right and (not (cell.up or cell.down) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                #ditto on right side
                if not right_edge:
                    right_edge = LineThing(x, y, y)
                else:
                    right_edge.v2 = y
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
                    top_edge = LineThing(y, x, x)
                else:
                    top_edge.v2 = x
            elif top_edge:
                #if we've found a cell without a top edge and the cell to the left had one, that must have been the end of that edge
                toplines.append(top_edge)
                top_edge = None
            if cell.down and ( not (cell.left or cell.right) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                #ditto downwards
                if not bottom_edge:
                    bottom_edge = LineThing(y, x, x)
                else:
                    bottom_edge.v2 = x
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
                    TL_edge = LineThing(x, y, y)
                else:
                    TL_edge.v2 = y
            elif TL_edge:
                TLlines.append(TL_edge)
                TL_edge = None
            if (cell.down and cell.right) and not (cell.up or cell.left):
                if not BR_edge:
                    BR_edge = LineThing(x, y, y)
                else:
                    BR_edge.v2 = y
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
                    TR_edge = LineThing(x, y, y)
                else:
                    TR_edge.v2 = y
            elif TR_edge:
                TRlines.append(TR_edge)
                TR_edge = None
            if cell.down and cell.left and not (cell.up or cell.right):
                if not BL_edge:
                    BL_edge = LineThing(x, y, y)
                else:
                    BL_edge.v2 = y
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
        pygame.draw.line(window, white, (line.i * 50, line.v1 * 50), (line.i * 50, (line.v2 + 1) * 50), 5)
    for line in rightlines:
        pygame.draw.line(window, white, ((line.i + 1) * 50, line.v1 * 50), ((line.i + 1) * 50, (line.v2 + 1) * 50), 5)
    for line in toplines:
        pygame.draw.line(window, white, (line.v1 * 50, line.i * 50), ((line.v2 + 1) * 50, line.i * 50), 5)
    for line in bottomlines:
        pygame.draw.line(window, white, (line.v1 * 50, (line.i + 1) * 50), ((line.v2 + 1) * 50, (line.i + 1) * 50), 5)
    for line in TRlines:
        pygame.draw.line(window, white, ((line.i + line.v1) * 50 - 900, line.v1 * 50), ((line.i + line.v2 + 1) * 50 - 900, (line.v2 + 1) * 50), 5)
    for line in BRlines:
        pygame.draw.line(window, white, ((line.i - line.v1 + 1) * 50, line.v1 * 50), ((line.i - line.v2) * 50, (line.v2 + 1) * 50), 5)
    for line in BLlines:
        pygame.draw.line(window, white, ((line.i + line.v1) * 50 - 900, line.v1 * 50), ((line.i + line.v2 + 1) * 50 - 900, (line.v2 + 1) * 50), 5)
    for line in TLlines:
        pygame.draw.line(window, white, ((line.i - line.v1 + 1) * 50, line.v1 * 50), ((line.i - line.v2) * 50, (line.v2 + 1) * 50), 5)

def draw_pointer():
    pygame.draw.circle(window, green, (pointer_x, pointer_y), 20)
    mouse = pygame.mouse.get_pos()
    pygame.draw.line(window, green, (pointer_x, pointer_y), mouse)
    x = pointer_x/50
    y = pointer_y/50
    dx = (mouse[0] - pointer_x)/50
    dy = (mouse[1] - pointer_y)/50
    x2 = x + dx
    y2 = y + dy
    value = check_collision(x, y, dx, dy)
    intersections = []
    # if value:
    #     cx, cy, x2, y2 = value
    #     intersections.append((cx * 50, cy * 50))
    while value:
        cx, cy, x2, y2 = value
        intersections.append((cx * 50, cy * 50))
        dx = x2 - cx
        dy = y2 - cy
        value = check_collision(cx, cy, dx, dy)
    intersections.append((x2 * 50, y2 * 50))
    for x, point in enumerate(intersections[:-1]):
        pygame.draw.circle(window, pink, point, 5)
        pygame.draw.line(window, blue, point, intersections[x+1], 2)
    pygame.draw.circle(window, cyan, intersections[-1], 10)

def first_greater(arr, target):
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
    if dx > 0 and leftlines:
        #left edges
        start_index = first_greater(leftlines, x)
        end_index = last_smaller(leftlines, x + dx)
        for i in range(start_index, end_index + 1):
            line = leftlines[i]
            if horizontal:
                yval = y
            else:
                yval = line.i * slope + c
            if line.v1 <= yval <= line.v2 + 1:
                intersection = True
                cx = line.i
                cy = yval
                direction = "left"
                break
    elif dx < 0 and rightlines:
        #right edges
        start_index = first_greater(rightlines, x + dx - 1)
        end_index = last_smaller(rightlines, x - 1)
        for i in reversed(range(start_index, end_index + 1)):
            line = rightlines[i]
            if horizontal:
                yval = y
            else:
                yval = (line.i + 1) * slope + c
            if line.v1 <= yval <= (line.v2 + 1):
                intersection = True
                cx = line.i + 1
                cy = yval
                direction = "right"
                break
    if dy > 0 and toplines:
        #top edges
        start_index = first_greater(toplines, y)
        if intersection:
            end_index = last_smaller(toplines, cy)
        else:
            end_index = last_smaller(toplines, y + dy)
        for i in range(start_index, end_index + 1):
            line = toplines[i]
            if vertical:
                xval = x
            else:
                xval = (line.i - c) / slope
            if line.v1 <= xval <= line.v2 + 1:
                if not intersection or cy > line.i:
                    intersection = True
                    cx = xval
                    cy = line.i
                    direction = "up"
                break
    elif dy < 0 and bottomlines:
        #bottom edge
        if intersection:
            start_index = first_greater(bottomlines, cy - 1)
        else:
            start_index = first_greater(bottomlines, y + dy - 1)
        end_index = last_smaller(bottomlines, y - 1)
        for i in reversed(range(start_index, end_index + 1)):
            line = bottomlines[i]
            if vertical:
                xval = x
            else:
                xval = ((line.i + 1) - c) / slope
            if line.v1 <= xval <= (line.v2 + 1):
                if not intersection or cy < line.i + 1:
                    intersection = True
                    cx = xval
                    cy = line.i + 1
                    direction = "down"
                break
    # now we check against the diagonals...
    # for any given direction at most 2 of the diagonal directions need checking.
    if dy < dx and BLlines:
        offset = 18
        #BL lines
        start_index = first_greater(BLlines, (x - y) + offset)
        if intersection:
            end_index = last_smaller(BLlines, (cx - cy) + offset)
        else:
            end_index = last_smaller(BLlines, ((x + dx) - (y + dy)) + offset)
        for i in range(start_index, end_index + 1):
            line = BLlines[i]
            b = -line.i + offset
            if vertical:
                xval = x
            else:
                xval = (b - c) / (slope - 1)
            if horizontal:
                yval = y
            else:
                yval = xval + b
            if line.v1 <= yval <= (line.v2 + 1):
                if not intersection or cx - cy > xval - yval:
                    intersection = True
                    cx = xval
                    cy = yval
                    direction = "down/left"
                break
    elif dy > dx and TRlines:
        offset = 18
        #TR lines
        if intersection:
            start_index = first_greater(TRlines, (cx - cy) + offset)
        else:
            start_index = first_greater(TRlines, ((x + dx) - (y + dy)) + offset)
        end_index = last_smaller(TRlines, (x - y) + offset)
        for i in reversed(range(start_index, end_index + 1)):
            line = TRlines[i]
            b = -line.i + offset
            if vertical:
                xval = x
            else:
                xval = (b - c) / (slope - 1)
            if horizontal:
                yval = y
            else:
                yval = xval + b
            if line.v1 <= yval <= (line.v2 + 1):
                if not intersection or cx - cy < xval - yval:
                    intersection = True
                    cx = xval
                    cy = yval
                    direction = "up/right"
                break
    if dy > -dx and TLlines:
        #TL lines
        start_index = first_greater(TLlines, (x + y) - 1)
        if intersection:
            end_index = last_smaller(TLlines, (cx + cy) - 1)
        else:
            end_index = last_smaller(TLlines, ((x + dx) + (y + dy)) - 1)
        for i in range(start_index, end_index + 1):
            line = TLlines[i]
            b = line.i + 1
            if vertical:
                xval = x
            else:
                xval = (b - c) / (slope + 1)
            if horizontal:
                yval = y
            else:
                yval = -xval + b
            if line.v1 <= yval <= line.v2 + 1:
                if not intersection or cx + cy > xval + yval:
                    intersection = True
                    cx = xval
                    cy = yval
                    direction = "up/left"
                break
    elif dy < -dx and BRlines:
        #BR lines
        if intersection:
            start_index = first_greater(BRlines, (cx + cy) - 1)
        else:
            start_index = first_greater(BRlines, ((x + dx) + (y + dy))  - 1)
        end_index = last_smaller(BRlines, (x + y) - 1)
        for i in reversed(range(start_index, end_index + 1)):
            line = BRlines[i]
            b = line.i + 1
            if vertical:
                xval = x
            else:
                xval = (b - c) / (slope + 1)
            if horizontal:
                yval = y
            else:
                yval = -xval + b
            if line.v1 <= yval <= (line.v2 + 1):
                if not intersection or cx + cy < xval + yval:
                    intersection = True
                    cx = xval
                    cy = yval
                    direction = "down/right"
                break
    if intersection:
        if direction == "up" or direction == "down":
            x2 = x + dx
            y2 = cy - ((y+dy) - cy)
        elif direction == "left" or direction == "right":
            x2 = cx - ((x+dx) - cx)
            y2 = y + dy
        elif direction == "up/left" or direction == "down/right":
            x2 = cx + cy - (y+dy)
            y2 = cy + cx - (x+dx)
        else:
            assert(direction == "down/left" or direction == "up/right")
            x2 = cx - cy + (y+dy)
            y2 = cy - cx + (x+dx)
        return cx, cy, x2, y2
    else:
        return False

def print_everything():
    print(f"x : {pointer_x/50}")
    print(f"y : {pointer_y/50}")
    mouse = pygame.mouse.get_pos()
    print(f"dx : {(mouse[0] - pointer_x)/50}")
    print(f"dy : {(mouse[1] - pointer_y)/50}")
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
    print(check_collision(pointer_x/50, pointer_y/50, (mouse[0] - pointer_x)/50, (mouse[1] - pointer_y)/50))

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
        grid[int(pos[0]/50)][int(pos[1]/50)] = True
        scan_edges()
        make_lines()
    elif buttons[2]:
        grid[int(pos[0]/50)][int(pos[1]/50)] = False
        scan_edges()
        make_lines()
    draw_grid()
    draw_edgemap()
    draw_lines()
    draw_pointer()
    pygame.display.update()