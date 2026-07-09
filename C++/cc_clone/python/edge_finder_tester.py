import pygame
import random
import math

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
CHUNK_SIZE = 8

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
    def __init__(self, north = None, south = None, east = None, west = None):
        self.grid = []
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.toplines = []
        self.bottomlines = []
        self.leftlines = []
        self.rightlines = []
        self.TLlines = []
        self.TRlines = []
        self.BLlines = []
        self.BRlines = []
        self.has_lines = False
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

    def draw_lines(self, offset_x, offset_y):
        for line in self.leftlines:
            pygame.draw.line(window, white, (line.i * TILE_SIZE + offset_x, line.v1 * TILE_SIZE + offset_y), (line.i * TILE_SIZE + offset_x, (line.v2) * TILE_SIZE + offset_y), 5)
        for line in self.rightlines:
            pygame.draw.line(window, white, ((line.i) * TILE_SIZE + offset_x, line.v1 * TILE_SIZE + offset_y), (line.i * TILE_SIZE + offset_x, (line.v2) * TILE_SIZE + offset_y), 5)
        for line in self.toplines:
            pygame.draw.line(window, white, (line.v1 * TILE_SIZE + offset_x, line.i * TILE_SIZE + offset_y), (line.v2 * TILE_SIZE + offset_x, line.i * TILE_SIZE + offset_y), 5)
        for line in self.bottomlines:
            pygame.draw.line(window, white, (line.v1 * TILE_SIZE + offset_x, (line.i) * TILE_SIZE + offset_y), (line.v2 * TILE_SIZE + offset_x, line.i * TILE_SIZE + offset_y), 5)
        for line in self.TRlines:
            pygame.draw.line(window, white, ((line.i + line.v1) * TILE_SIZE + offset_x, line.v1 * TILE_SIZE + offset_y), ((line.i + line.v2) * TILE_SIZE + offset_x, (line.v2) * TILE_SIZE + offset_y), 5)
        for line in self.BRlines:
            pygame.draw.line(window, white, ((line.i - line.v1) * TILE_SIZE + offset_x, line.v1 * TILE_SIZE + offset_y), ((line.i - line.v2) * TILE_SIZE + offset_x, line.v2 * TILE_SIZE + offset_y), 5)
        for line in self.BLlines:
            pygame.draw.line(window, white, ((line.i + line.v1) * TILE_SIZE + offset_x, line.v1 * TILE_SIZE + offset_y), ((line.i + line.v2) * TILE_SIZE + offset_x, (line.v2) * TILE_SIZE + offset_y), 5)
        for line in self.TLlines:
            pygame.draw.line(window, white, ((line.i - line.v1) * TILE_SIZE + offset_x , line.v1* TILE_SIZE + offset_y), ((line.i - line.v2) * TILE_SIZE + offset_x, line.v2 * TILE_SIZE + offset_y), 5)

    def scan_edges(self):
        edgemap = []
        for x, row in enumerate(self.grid):
            edgemap.append([])
            for y, cell in enumerate(row):
                edgemap[-1].append(EdgeThing())
                if cell:
                    if x > 0:
                        edgemap[x][y].left = not self.grid[x-1][y]
                    elif self.west:
                        edgemap[x][y].left = not self.west.grid[CHUNK_SIZE - 1][y]
                    if x < CHUNK_SIZE - 1:
                        edgemap[x][y].right = not self.grid[x+1][y]
                    elif self.east:
                        edgemap[x][y].right = not self.east.grid[0][y]
                    if y > 0:
                        edgemap[x][y].up = not self.grid[x][y-1]
                    elif self.north:
                        edgemap[x][y].up = not self.north.grid[x][CHUNK_SIZE - 1]
                    if y < CHUNK_SIZE - 1:
                        edgemap[x][y].down = not self.grid[x][y+1]
                    elif self.south:
                        edgemap[x][y].down = not self.south.grid[x][0]
                else:
                    edgemap[x][y] = EdgeThing()
        self.toplines.clear()
        self.bottomlines.clear()
        self.leftlines.clear()
        self.rightlines.clear()
        self.TLlines.clear()
        self.TRlines.clear()
        self.BLlines.clear()
        self.BRlines.clear()
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
                    self.leftlines.append(left_edge)
                    left_edge = None
                if cell.right and (not (cell.up or cell.down) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                    #ditto on right side
                    if not right_edge:
                        right_edge = LineThing(x+1, y, y+1)
                    else:
                        right_edge.v2 = y+1
                elif right_edge:
                    self.rightlines.append(right_edge)
                    right_edge = None
            #make sure when you reach the end of the scan you don't carry a line onto the next iteration
            if left_edge:
                self.leftlines.append(left_edge)
                left_edge = None
            if right_edge:
                self.rightlines.append(right_edge)
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
                    self.toplines.append(top_edge)
                    top_edge = None
                if cell.down and ( not (cell.left or cell.right) or sum([cell.left, cell.right, cell.up, cell.down]) > 2):
                    #ditto downwards
                    if not bottom_edge:
                        bottom_edge = LineThing(y+1, x, x+1)
                    else:
                        bottom_edge.v2 = x+1
                elif bottom_edge:
                    self.bottomlines.append(bottom_edge)
                    bottom_edge = None
            if top_edge:
                self.toplines.append(top_edge)
                top_edge = None
            if bottom_edge:
                self.bottomlines.append(bottom_edge)
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
                    self.TLlines.append(TL_edge)
                    TL_edge = None
                if (cell.down and cell.right) and not (cell.up or cell.left):
                    if not BR_edge:
                        BR_edge = LineThing(x+1, y, y+1)
                    else:
                        BR_edge.v2 = y+1
                elif BR_edge:
                    self.BRlines.append(BR_edge)
                    BR_edge = None
            if TL_edge:
                    self.TLlines.append(TL_edge)
                    TL_edge = None
            if BR_edge:
                self.BRlines.append(BR_edge)
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
                    self.TRlines.append(TR_edge)
                    TR_edge = None
                if cell.down and cell.left and not (cell.up or cell.right):
                    if not BL_edge:
                        BL_edge = LineThing(x-offset, y, y+1)
                    else:
                        BL_edge.v2 = y+1
                elif BL_edge:
                    self.BLlines.append(BL_edge)
                    BL_edge = None
            if TR_edge:
                    self.TRlines.append(TR_edge)
                    TR_edge = None
            if BL_edge:
                    self.BLlines.append(BL_edge)
                    BL_edge = None
        self.has_lines = (self.toplines or self.bottomlines or self.leftlines or self.rightlines or self.TLlines or self.TRlines or self.BLlines or self.BRlines)

    def check_collision(self, x, y, dx, dy):
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
        if dx > 0 and self.leftlines:
            index_1 = first_greater(self.leftlines, x)
            end_1 = len(self.leftlines) - 1
            lines_1 = self.leftlines
            step_1 = 1
        elif dx < 0 and self.rightlines:
            index_1 = last_smaller(self.rightlines, x)
            end_1 = 0
            lines_1 = self.rightlines
            step_1 = -1
        else:
            step_1 = 0
            index_1 = 0
        if dy > 0 and self.toplines:
            index_2 = first_greater(self.toplines, y)
            end_2 = len(self.toplines) - 1
            lines_2 = self.toplines
            step_2 = 1
        elif dy < 0 and self.bottomlines:
            index_2 = last_smaller(self.bottomlines, y)
            end_2 = 0
            lines_2 = self.bottomlines
            step_2 = -1
        else:
            step_2 = 0
            index_2 = 0
        if dy < dx and self.BLlines:
            index_3 = first_greater(self.BLlines, x - y)
            end_3 = len(self.BLlines) - 1
            lines_3 = self.BLlines
            step_3 = 1
        elif dy > dx and self.TRlines:
            index_3 = last_smaller(self.TRlines, x - y)
            end_3 = 0
            lines_3 = self.TRlines
            step_3 = -1
        else:
            step_3 = 0
            index_3 = 0
        if dy > -dx and self.TLlines:
            index_4 = first_greater(self.TLlines, x + y)
            end_4 = len(self.TLlines) - 1
            lines_4 = self.TLlines
            step_4 = 1
        elif dy < -dx and self.BRlines:
            index_4 = last_smaller(self.BRlines, x + y)
            end_4 = 0
            lines_4 = self.BRlines
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

chunks = []
# edgemap = []

for x in range(int(SCREEN_WIDTH / (TILE_SIZE * CHUNK_SIZE))):
    chunks.append([])
    for y in range(int(SCREEN_HEIGHT / (TILE_SIZE * CHUNK_SIZE))):
        chunks[-1].append(Chunk())

for x, row in enumerate(chunks):
    for y, chunk in enumerate(row):
        if x > 0:
            chunk.west = chunks[x-1][y]
            chunks[x-1][y].east = chunk
        if y > 0:
            chunk.north = chunks[x][y-1]
            chunks[x][y-1].south = chunk


pointer_x = 100.0
pointer_y = 100.0

# self.toplines = []
# self.bottomlines = []
# self.leftlines = []
# self.rightlines = []
# self.TLlines = []
# self.TRlines = []
# self.BLlines = []
# self.BRlines = []

def draw_chunks():
    for x, row in enumerate(chunks):
        for y, chunk in enumerate(row):
            chunk.draw(x * (TILE_SIZE * CHUNK_SIZE), y * (TILE_SIZE * CHUNK_SIZE))
            chunk.draw_lines(x * (TILE_SIZE * CHUNK_SIZE), y * (TILE_SIZE * CHUNK_SIZE))

def draw_pointer():
    pygame.draw.circle(window, green, (pointer_x, pointer_y), 20)
    mouse = pygame.mouse.get_pos()
    # pygame.draw.line(window, green, (pointer_x, pointer_y), mouse)
    xi = pointer_x/TILE_SIZE
    yi = pointer_y/TILE_SIZE
    dx = (mouse[0] - pointer_x)/TILE_SIZE
    dy = (mouse[1] - pointer_y)/TILE_SIZE
    x2 = (xi + dx) * TILE_SIZE
    y2 = (yi + dy) * TILE_SIZE
    intersections = [(pointer_x, pointer_y)]
    x_abs = pointer_x / (TILE_SIZE * CHUNK_SIZE)
    y_abs = pointer_y / (TILE_SIZE * CHUNK_SIZE)
    x_rel = (mouse[0] - pointer_x) / (TILE_SIZE * CHUNK_SIZE)
    y_rel = (mouse[1] - pointer_y) / (TILE_SIZE * CHUNK_SIZE)
    intersected_chunks = check_c(x_abs, y_abs, x_rel, y_rel)
    i = 0
    while i < len(intersected_chunks):
        chunk_pair = intersected_chunks[i]
        chunk_pos_x = chunk_pair[0] * CHUNK_SIZE
        chunk_pos_y = chunk_pair[1] * CHUNK_SIZE
        rect = (chunk_pos_x * TILE_SIZE, chunk_pos_y * TILE_SIZE, TILE_SIZE * CHUNK_SIZE, TILE_SIZE * CHUNK_SIZE)
        if chunk_pair[0] < 0 or chunk_pair[1] < 0 or chunk_pair[1] > len(chunks) -1 or chunk_pair[1] > len(chunks[0]) -1:
            i += 1
            continue
        chunk = chunks[chunk_pair[0]][chunk_pair[1]]
        if chunk.has_lines:
            value = chunk.check_collision(xi - chunk_pos_x, yi - chunk_pos_y, dx, dy)
            if value:
                pygame.draw.rect(window, green, rect, 4)
                cx, cy, x2, y2 = value
                dx = x2 - cx
                dy = y2 - cy
                xi = (cx + chunk_pos_x)
                yi = (cy + chunk_pos_y)
                x2 = (x2 + chunk_pos_x) * TILE_SIZE
                y2 = (y2 + chunk_pos_y) * TILE_SIZE
                intersected_chunks = check_c((cx + chunk_pos_x) / CHUNK_SIZE, (cy + chunk_pos_y) / CHUNK_SIZE, dx / CHUNK_SIZE, dy / CHUNK_SIZE)
                i = 0
                intersections.append((xi * TILE_SIZE, yi * TILE_SIZE))
                continue
            else:
                pygame.draw.rect(window, yellow, rect, 2)
        else:
            pygame.draw.rect(window, cyan, rect, 2)
        i += 1
    intersections.append((x2, y2))
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

def check_c(x, y, dx, dy):
    points = [(math.floor(x), math.floor(y))]
    xstep = 1 if dx > 0 else -1
    ystep = 1 if dy > 0 else -1
    i = math.floor(x)
    j = math.floor(y)
    m = dy / dx if dx != 0 else None
    c = y - (m * x) if m else None
    if i == math.floor(x + dx) and j == math.floor(y + dy):
        return points
    elif dy == 0:
        while i != math.floor(x + dx):
            i += xstep
            points.append((i, math.floor(y)))
    elif dx == 0:
        while j != math.floor(y + dy):
            j += ystep
            points.append((math.floor(x), j))
    elif dy > 0 and dx > 0:
        while i != math.floor(x + dx) or j != math.floor(y + dy):
            if m * (i + xstep) + c < j + ystep:
                i += xstep
            else:
                j += ystep
            points.append((i, j))
    elif dy < 0 and dx > 0:
        while i != math.floor(x + dx) or j != math.floor(y + dy):
            if m * (i + xstep) + c >= j:
                i += xstep
            else:
                j += ystep
            points.append((i, j))
    elif dy > 0 and dx < 0:
        while i != math.floor(x + dx) or j != math.floor(y + dy):
            if m * i + c < j + ystep:
                i += xstep
            else:
                j += ystep
            points.append((i, j))
    elif dy < 0 and dx < 0:
        while i != math.floor(x + dx) or j != math.floor(y + dy):
            if m * i + c >= j:
                i += xstep
            else:
                j += ystep
            points.append((i, j))
    return points

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("edge_finder_tester")
while True:
    window.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Click")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_UP:
                pointer_y -= 1
            if event.key == pygame.K_DOWN:
                pointer_y += 1
            if event.key == pygame.K_LEFT:
                pointer_x -= 1
            if event.key == pygame.K_RIGHT:
                pointer_x += 1
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
        chunks[chunk_x][chunk_y].scan_edges()
        if cell_x == 0 and chunks[chunk_x][chunk_y].west:
            chunks[chunk_x-1][chunk_y].scan_edges()
        elif cell_x == CHUNK_SIZE -1 and chunks[chunk_x][chunk_y].east:
            chunks[chunk_x+1][chunk_y].scan_edges()
        if cell_y == 0 and chunks[chunk_x][chunk_y].north:
            chunks[chunk_x][chunk_y-1].scan_edges()
        elif cell_y == CHUNK_SIZE -1 and chunks[chunk_x][chunk_y].south:
            chunks[chunk_x][chunk_y+1].scan_edges()
    elif buttons[2]:
        chunks[chunk_x][chunk_y].grid[cell_x][cell_y] = False
        chunks[chunk_x][chunk_y].scan_edges()
        if cell_x == 0 and chunks[chunk_x][chunk_y].west:
            chunks[chunk_x-1][chunk_y].scan_edges()
        elif cell_x == CHUNK_SIZE -1 and chunks[chunk_x][chunk_y].east:
            chunks[chunk_x+1][chunk_y].scan_edges()
        if cell_y == 0 and chunks[chunk_x][chunk_y].north:
            chunks[chunk_x][chunk_y-1].scan_edges()
        elif cell_y == CHUNK_SIZE -1 and chunks[chunk_x][chunk_y].south:
            chunks[chunk_x][chunk_y+1].scan_edges()
    draw_chunks()
    draw_pointer()
    pygame.display.update()