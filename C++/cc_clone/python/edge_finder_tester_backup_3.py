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

TILE_SIZE = 25
SCREEN_WIDTH = 64 * TILE_SIZE
SCREEN_HEIGHT = 32 * TILE_SIZE
CHUNK_SIZE = 16

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

class Chunk:
    def __init__(self):
        self.grid = []
        self.toplines = []
        self.bottomlines = []
        self.leftlines = []
        self.rightlines = []
        self.TLlines = []
        self.TRlines = []
        self.BLlines = []
        self.BRlines = []
        for _ in range(CHUNK_SIZE):
            self.grid.append([])
            for __ in range(CHUNK_SIZE):
                self.grid[-1].append(False)
    
    def draw(self, offset_x = 0, offset_y = 0):
        pygame.draw.line(window, red, (offset_x, offset_y), (offset_x + (TILE_SIZE * CHUNK_SIZE), offset_y))
        pygame.draw.line(window, red, (offset_x, offset_y), (offset_x, offset_y + (TILE_SIZE * CHUNK_SIZE)))
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(window, grey, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE))

    def scan_edges():
        pass

chunks = []
# edgemap = []

for x in range(int(SCREEN_WIDTH / (TILE_SIZE * CHUNK_SIZE))):
    chunks.append([])
    # edgemap.append([])
    for y in range(int(SCREEN_HEIGHT / (TILE_SIZE * CHUNK_SIZE))):
        chunks[-1].append(Chunk())
        # edgemap[-1].append(EdgeThing())

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

def draw_chunks():
    for x, row in enumerate(chunks):
        for y, chunk in enumerate(row):
            chunk.draw(x * (TILE_SIZE * CHUNK_SIZE), y * (TILE_SIZE * CHUNK_SIZE))

# def scan_edges():
#     for x, row in enumerate(grid):
#         for y, cell in enumerate(row):
#             if cell:
#                 if x > 0:
#                     edgemap[x][y].left = not grid[x-1][y] if x-1 >= 0 else False
#                 if x < int(SCREEN_WIDTH / TILE_SIZE):
#                     edgemap[x][y].right = not grid[x+1][y] if x+1 < len(grid) else False
#                 if y > 0:
#                     edgemap[x][y].up = not grid[x][y-1] if y-1 >= 0 else False
#                 if y < int(SCREEN_HEIGHT / TILE_SIZE):
#                     edgemap[x][y].down = not grid[x][y+1] if y+1 < len(grid[x]) else False
#             else:
#                 edgemap[x][y] = EdgeThing()
#     toplines.clear()
#     bottomlines.clear()
#     leftlines.clear()
#     rightlines.clear()
#     TLlines.clear()
#     TRlines.clear()
#     BLlines.clear()
#     BRlines.clear()
#     #4 passes, scan for vertical lines, then horizontal, then each diagonal
#     #vertical scan first
#     left_edge = None
#     right_edge = None
#     for x, row in enumerate(edgemap):
#         for y, cell in enumerate(row):
#             if cell.left and (not (cell.up or cell.down) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
#                 #if we've found a cell with a left edge, it either is the top of the edge or it extends the same line as the cell above
#                 if not left_edge:
#                     left_edge = LineThing(x, y, y+1)
#                 else:
#                     left_edge.v2 = y+1
#             elif left_edge:
#                 #if we've found a cell without a left edge and the cell above had one, that must have been the end of that edge
#                 leftlines.append(left_edge)
#                 left_edge = None
#             if cell.right and (not (cell.up or cell.down) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
#                 #ditto on right side
#                 if not right_edge:
#                     right_edge = LineThing(x+1, y, y+1)
#                 else:
#                     right_edge.v2 = y+1
#             elif right_edge:
#                 rightlines.append(right_edge)
#                 right_edge = None
#         #make sure when you reach the end of the scan you don't carry a line onto the next iteration
#         if left_edge:
#             leftlines.append(left_edge)
#             left_edge = None
#         if right_edge:
#             rightlines.append(right_edge)
#             right_edge = None
#     #horizontal scan
#     top_edge = None
#     bottom_edge = None
#     for y in range(len(edgemap[0])):
#         for x, row in enumerate(edgemap):
#             cell = row[y]
#             if cell.up and (not (cell.left or cell.right) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
#                 #if we've found a cell with a top edge, it either is the left end of the edge or it extends the same line as the cell to the left
#                 if not top_edge:
#                     top_edge = LineThing(y, x, x+1)
#                 else:
#                     top_edge.v2 = x+1
#             elif top_edge:
#                 #if we've found a cell without a top edge and the cell to the left had one, that must have been the end of that edge
#                 toplines.append(top_edge)
#                 top_edge = None
#             if cell.down and ( not (cell.left or cell.right) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
#                 #ditto downwards
#                 if not bottom_edge:
#                     bottom_edge = LineThing(y+1, x, x+1)
#                 else:
#                     bottom_edge.v2 = x+1
#             elif bottom_edge:
#                 bottomlines.append(bottom_edge)
#                 bottom_edge = None
#         if top_edge:
#             toplines.append(top_edge)
#             top_edge = None
#         if bottom_edge:
#             bottomlines.append(bottom_edge)
#             bottom_edge = None
#     #now the fun begins with the diagonal scans...
#     # / this way first /
#     TL_edge = None
#     BR_edge = None
#     for x in range(len(edgemap) + len(edgemap[0])):
#         for y in range(len(edgemap[0])):
#             if x - y < 0 or x - y >= len(edgemap):
#                 continue
#             cell = edgemap[x-y][y]
#             if (cell.up and cell.left) and not (cell.down or cell.right):
#                 #if we've found a cell with a top left edge, it's either a new edge or it continues the line of the cell to the top right
#                 if not TL_edge:
#                     TL_edge = LineThing(x+1, y, y+1)
#                 else:
#                     TL_edge.v2 = y+1
#             elif TL_edge:
#                 TLlines.append(TL_edge)
#                 TL_edge = None
#             if (cell.down and cell.right) and not (cell.up or cell.left):
#                 if not BR_edge:
#                     BR_edge = LineThing(x+1, y, y+1)
#                 else:
#                     BR_edge.v2 = y+1
#             elif BR_edge:
#                 BRlines.append(BR_edge)
#                 BR_edge = None
#         if TL_edge:
#                 TLlines.append(TL_edge)
#                 TL_edge = None
#         if BR_edge:
#             BRlines.append(BR_edge)
#             BR_edge = None
#     # \ now this way \
#     TR_edge = None
#     BL_edge = None
#     offset = len(edgemap[0])
#     for x in range(len(edgemap) + len(edgemap[0])):
#         for y in range(len(edgemap[0])):
#             if x - offset + y < 0 or x - offset + y >= len(edgemap):
#                 continue
#             cell = edgemap[x - offset + y][y]
#             if cell.up and cell.right and not (cell.down or cell.left):
#                 if not TR_edge:
#                     TR_edge = LineThing(x-offset, y, y+1)
#                 else:
#                     TR_edge.v2 = y+1
#             elif TR_edge:
#                 TRlines.append(TR_edge)
#                 TR_edge = None
#             if cell.down and cell.left and not (cell.up or cell.right):
#                 if not BL_edge:
#                     BL_edge = LineThing(x-offset, y, y+1)
#                 else:
#                     BL_edge.v2 = y+1
#             elif BL_edge:
#                 BLlines.append(BL_edge)
#                 BL_edge = None
#         if TR_edge:
#                 TRlines.append(TR_edge)
#                 TR_edge = None
#         if BL_edge:
#                 BLlines.append(BL_edge)
#                 BL_edge = None

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
    if dx != 0 and dy != 0:
        slope = dy/dx
        c = y - slope * x
    elif dx == 0:
        vertical = True
        slope = None
    else:
        assert(dy == 0)
        slope = 0
        c = y
    end_x = x + dx
    end_y = y + dy
    #phase 1: preparing to do the loops
    if dx > 0 and leftlines:
        index_1 = first_greater(leftlines, x)
        end_1 = len(leftlines) - 1
        lines_1 = leftlines
        step_1 = 1
    elif dx < 0 and rightlines:
        index_1 = last_smaller(rightlines, x)
        end_1 = 0
        lines_1 = rightlines
        step_1 = -1
    else:
        step_1 = 0
        index_1 = 0
    if dy > 0 and toplines:
        index_2 = first_greater(toplines, y)
        end_2 = len(toplines) - 1
        lines_2 = toplines
        step_2 = 1
    elif dy < 0 and bottomlines:
        index_2 = last_smaller(bottomlines, y)
        end_2 = 0
        lines_2 = bottomlines
        step_2 = -1
    else:
        step_2 = 0
        index_2 = 0
    if dy < dx and BLlines:
        index_3 = first_greater(BLlines, x - y)
        end_3 = len(BLlines) - 1
        lines_3 = BLlines
        step_3 = 1
    elif dy > dx and TRlines:
        index_3 = last_smaller(TRlines, x - y)
        end_3 = 0
        lines_3 = TRlines
        step_3 = -1
    else:
        step_3 = 0
        index_3 = 0
    if dy > -dx and TLlines:
        index_4 = first_greater(TLlines, x + y)
        end_4 = len(TLlines) - 1
        lines_4 = TLlines
        step_4 = 1
    elif dy < -dx and BRlines:
        index_4 = last_smaller(BRlines, x + y)
        end_4 = 0
        lines_4 = BRlines
        step_4 = -1
    else:
        step_4 = 0
        index_4 = 0
    #phase 2: another thing I don't know how to describe...
    # basically you either index forwards or backwards depending on which sign dy has
    # next_1, ... next_4 are the y values normally
    # but if dy == 0 then you have to do phase 3 differently and use the x values instead
    if dy != 0:
        if (step_1 == 1 and index_1 <= end_1) or (step_1 == -1 and index_1 >= end_1):
            next_1 = lines_1[index_1].i * slope + c
        else:
            next_1 = end_y
        if (step_2 == 1 and index_2 <= end_2) or (step_2 == -1 and index_2 >= end_2):
            next_2 = lines_2[index_2].i
        else:
            next_2 = end_y
        if (step_3 == 1 and index_3 <= end_3) or (step_3 == -1 and index_3 >= end_3):
            if vertical:
                xval = x
            elif slope == 1:
                xval = (lines_3[index_3].i + c) / 2
            else:
                xval = -(lines_3[index_3].i + c) / (slope - 1)
            next_3 = xval - lines_3[index_3].i
        else:
            next_3 = end_y
        if (step_4 == 1 and index_4 <= end_4) or (step_4 == -1 and index_4 >= end_4):
            if vertical:
                xval = x
            elif slope == -1:
                xval = (lines_4[index_4].i - c) / 2
            else:
                xval = (lines_4[index_4].i - c) / (slope + 1)
            next_4 = lines_4[index_4].i - xval
        else:
            next_4 = end_y
    else:
        #slope = 0
        if (step_1 == 1 and index_1 <= end_1) or (step_1 == -1 and index_1 >= end_1):
            next_1 = lines_1[index_1].i
        else:
            next_1 = end_x
        #no need to check horizontal lines
        if (step_3 == 1 and index_3 <= end_3) or (step_3 == -1 and index_3 >= end_3):
            next_3 = lines_3[index_3].i + c
        else:
            next_3 = end_x
        if (step_4 == 1 and index_4 <= end_4) or (step_4 == -1 and index_4 >= end_4):
            next_4 = lines_4[index_4].i - c
        else:
            next_4 = end_x
    #phase 3: doing the loops when dy != 0
    looping = True
    if dy != 0:
        while looping:
            looping = False
            while (dy > 0 and next_1 < end_y and next_1 == min(next_1, next_2, next_3, next_4)) or (dy < 0 and next_1 > end_y and next_1 == max(next_1, next_2, next_3, next_4)):
                looping = True
                line = lines_1[index_1]
                if line.v1 <= next_1 <= line.v2:
                    cx = line.i
                    cy = next_1
                    x2 = 2 * cx - (x+dx)
                    y2 = y + dy
                    return cx, cy, x2, y2
                if index_1 != end_1:
                    index_1 += step_1
                    next_1 = lines_1[index_1].i * slope + c
                else:
                    next_1 = end_y
            while (dy > 0 and next_2 < end_y and next_2 == min(next_1, next_2, next_3, next_4)) or (dy < 0 and next_2 > end_y and next_2 == max(next_1, next_2, next_3, next_4)):
                looping = True
                line = lines_2[index_2]
                xval = x if vertical else (line.i - c) / slope
                if line.v1 <= xval <= line.v2:
                    cx = xval
                    cy = line.i
                    x2 = x + dx
                    y2 = 2 * cy - (y+dy)
                    return cx, cy, x2, y2
                if index_2 != end_2:
                    index_2 += step_2
                    next_2 = lines_2[index_2].i
                else:
                    next_2 = end_y
            while (dy > 0 and next_3 < end_y and next_3 == min(next_1, next_2, next_3, next_4)) or (dy < 0 and next_3 > end_y and next_3 == max(next_1, next_2, next_3, next_4)):
                looping = True
                line = lines_3[index_3]
                if line.v1 <= next_3 <= line.v2:
                    cx = next_3 + line.i
                    cy = next_3
                    x2 = cx - cy + (y+dy)
                    y2 = cy - cx + (x+dx)
                    return cx, cy, x2, y2
                if index_3 != end_3:
                    index_3 += step_3
                    if vertical:
                        xval = x
                    elif slope == 1:
                        xval = (lines_3[index_3].i + c) / 2
                    else:
                        xval = -(lines_3[index_3].i + c) / (slope - 1)
                    next_3 = xval - lines_3[index_3].i
                else:
                    next_3 = end_y
            while (dy > 0 and next_4 < end_y and next_4 == min(next_1, next_2, next_3, next_4)) or (dy < 0 and next_4 > end_y and next_4 == max(next_1, next_2, next_3, next_4)):
                looping = True
                line = lines_4[index_4]
                if line.v1 <= next_4 <= line.v2:
                    cx = line.i - next_4 
                    cy = next_4
                    x2 = cx + cy - (y+dy)
                    y2 = cy + cx - (x+dx)
                    return cx, cy, x2, y2
                if index_4 != end_4:
                    index_4 += step_4
                    if vertical:
                        xval = x
                    elif slope == -1:
                        xval = (lines_4[index_4].i - c) / 2
                    else:
                        xval = (lines_4[index_4].i - c) / (slope + 1)
                    next_4 = lines_4[index_4].i - xval
                else:
                    next_4 = end_y
        return False
    else:
        #when dy == 0
        while looping:
            looping = False
            while (dx > 0 and next_1 < end_x and next_1 == min(next_1, next_3, next_4)) or (dx < 0 and next_1 > end_x and next_1 == max(next_1, next_3, next_4)):
                looping = True
                line = lines_1[index_1]
                if line.v1 <= y <= line.v2:
                    x2 = 2 * next_1 - (x+dx)
                    return next_1, y, x2, y
                if index_1 != end_1:
                    index_1 += step_1
                    next_1 = lines_1[index_1].i
                else:
                    next_1 = end_x
            #no need to check horizontal lines
            while (dx > 0 and next_3 < end_x and next_3 == min(next_1, next_3, next_4)) or (dx < 0 and next_3 > end_x and next_3 == max(next_1, next_3, next_4)):
                looping = True
                line = lines_3[index_3]
                if line.v1 <= y <= line.v2:
                    x2 = next_3 - y + (y+dy)
                    y2 = y - next_3 + (x+dx)
                    return next_3, y, x2, y2
                if index_3 != end_3:
                    index_3 += step_3
                    next_3 = lines_3[index_3].i + c
                else:
                    next_3 = end_x
            while (dx > 0 and next_4 < end_x and next_4 == min(next_1, next_3, next_4)) or (dx < 0 and next_4 > end_x and next_4 == max(next_1, next_3, next_4)):
                looping = True
                line = lines_4[index_4]
                if line.v1 <= y <= line.v2:
                    x2 = next_4 + y - (y+dy)
                    y2 = y + next_4 - (x+dx)
                    return next_4, y, x2, y2
                if index_4 != end_4:
                    index_4 += step_4
                    next_4 = lines_4[index_4].i - c
                else:
                    next_4 = end_x
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
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
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
    chunk_x = int(pos[0] / (TILE_SIZE * CHUNK_SIZE))
    chunk_y = int(pos[1] / (TILE_SIZE * CHUNK_SIZE))
    cell_x = int(int(pos[0] % (TILE_SIZE * CHUNK_SIZE)) / TILE_SIZE)
    cell_y = int(int(pos[1] % (TILE_SIZE * CHUNK_SIZE)) / TILE_SIZE)
    if buttons[0]:
        chunks[chunk_x][chunk_y].grid[cell_x][cell_y] = True
    #     scan_edges()
    elif buttons[2]:
        chunks[chunk_x][chunk_y].grid[cell_x][cell_y] = False
    #     scan_edges()
    draw_chunks()
    draw_lines()
    draw_pointer()
    pygame.display.update()