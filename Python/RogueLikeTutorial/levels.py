import random
import entities
import math
import maffs

class Level:
    def __init__(self, size):
        self.start_pos = maffs.Point(int(size/2), int(size/2))
        self.size = size
        self.entities = []
        self.tiles = []
        self.visible_map = []
        for x in range(size):
            self.tiles.append([])
            self.visible_map.append([])
            for _ in range(size):
                self.tiles[x].append([])
                self.visible_map[x].append(None)
        self.ongoing_turn_actor = None

    def handle_turns(self):
        index = 0
        if self.ongoing_turn_actor != None and self.ongoing_turn_actor in entities.actor_components:
            index = entities.actor_components.index(self.ongoing_turn_actor)
        for actor in entities.actor_components[index:]:
            if actor.awake and actor.time_units <= 0:
                # only start an actors turn if their turn is actually starting here
                # they might be resuming their turn after a previous loop, so starting a new turn wouldn't make sense
                actor.start_turn()
            actor.do_turn()
            if actor.can_act:
                # if the actor can still act at the end of their turn (it's probably the player) then resume from here at the next loop
                # at some point the actor will finish their turn and looping may continue as normal
                self.ongoing_turn_actor = actor
                break
            else:
                self.ongoing_turn_actor = None

    def is_cell_in_bounds(self, pos):
        return 0 <= pos.x < self.size and 0 <= pos.y < self.size

    def add_entity(self, entity):
        entity.level = self
        self.entities.append(entity)
        self.tiles[entity.pos.x][entity.pos.y].append(entity)

    def add_entities(self, entities):
        for entity in entities:
            self.add_entity(entity)

    def move_entity(self, entity, new_pos):
        self.tiles[entity.pos.x][entity.pos.y].remove(entity)
        self.tiles[new_pos.x][new_pos.y].append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)
        self.tiles[entity.pos.x][entity.pos.y].remove(entity)

    def remove_entities(self, entities):
        for entity in entities:
            self.remove_entity(entity)

    def is_transparent_at(self, pos):
        transparent = True
        for entity in self.tiles[pos.x][pos.y]:
            if not entity.transparent:
                transparent = False
                break
        return transparent
    
    def get_blocking_entity_at(self, pos):
        output = None
        for entity in self.tiles[pos.x][pos.y]:
            if not entity.passable:
                output = entity
                break
        return output

    def is_passable_at(self, pos):
        passable = True
        for entity in self.tiles[pos.x][pos.y]:
            if not entity.passable:
                passable = False
                break
        return passable
    
    def get_grabbable_items_at(self, pos):
        return [item for item in self.tiles[pos.x][pos.y] if not item.rooted]

    def scan_LOS(self, pos):
        for x in range(self.size):
            for y in range(self.size):
                self.visible_map[x][y] = False
        self.visible_map[pos.x][pos.y] = True
        for quadrant in range(4):
            self.scan_quadrant(pos, 1, -1, 1, quadrant)

    def scan_quadrant(self, pos, depth, start_slope, end_slope, quadrant):
        prev_not_blocking = False
        prev_blocking = False
        min_col = math.floor(depth * start_slope + 0.5)
        max_col = math.ceil(depth * end_slope - 0.5)
        for i in range(max_col - min_col + 1):
            col = i + min_col
            if quadrant == 0:
                x = pos.x + col
                y = pos.y - depth
            if quadrant == 1:
                x = pos.x + col
                y = pos.y + depth
            if quadrant == 2:
                x = pos.x + depth
                y = pos.y + col
            if quadrant == 3:
                x = pos.x - depth
                y = pos.y + col
            blocking = not self.is_transparent_at(maffs.Point(x, y))
            symmetric = (col >= depth * start_slope and col <= depth * end_slope)
            if blocking or symmetric:
                self.visible_map[x][y] = True
            if prev_blocking and not blocking:
                start_slope = (2 * col - 1) * 1.0 / (2 * depth)
            if prev_not_blocking and blocking:
                self.scan_quadrant(pos, depth+1, start_slope, ((2 * col - 1) * 1.0 / (2 * depth)), quadrant)
            prev_not_blocking = not blocking
            prev_blocking = blocking
        if not prev_blocking:
            self.scan_quadrant(pos, depth + 1, start_slope, end_slope, quadrant)
    
    def path_find(self, start, end):
        if not self.is_cell_in_bounds(end):
            return False
        if start == end:
            return maffs.Point()
        vmap = []
        for x in range(self.size):
            vmap.append([])
            for y in range(self.size):
                if self.is_passable_at(maffs.Point(x, y)):
                    vmap[x].append("F")
                else:
                    vmap[x].append("W")
        vmap[start.x][start.y] = "F"
        vmap[end.x][end.y] = 0.0
        cells_to_process = [end]
        while cells_to_process:
            cell = cells_to_process[0]
            cell_value = vmap[cell.x][cell.y]
            directions = [
                maffs.Point(-1, -1),
                maffs.Point(-1,  0),
                maffs.Point(-1,  1),
                maffs.Point( 0, -1),
                maffs.Point( 0,  1),
                maffs.Point( 1, -1),
                maffs.Point( 1,  0),
                maffs.Point( 1,  1)]
            for direction in directions:
                other_cell = cell + direction
                if not self.is_cell_in_bounds(other_cell):
                    continue
                other_value = vmap[other_cell.x][other_cell.y]
                distance = maffs.true_distance(cell, other_cell)
                if vmap[other_cell.x][other_cell.y] == "F" or (type(other_value) == float and other_value > cell_value + distance):
                    vmap[other_cell.x][other_cell.y] = vmap[cell.x][cell.y] + distance
                    cells_to_process.append(other_cell)
            cells_to_process.remove(cell)
        if vmap[start.x][start.y] == "F":
            return False
        else:
            lowest = vmap[start.x][start.y]
            output = maffs.Point()
            directions = [
                maffs.Point(-1, -1),
                maffs.Point(-1,  0),
                maffs.Point(-1,  1),
                maffs.Point( 0, -1),
                maffs.Point( 0,  1),
                maffs.Point( 1, -1),
                maffs.Point( 1,  0),
                maffs.Point( 1,  1)]
            for direction in directions:
                value = vmap[start.x + direction.x][start.y + direction.y]
                if type(value) is float and value < lowest:
                    output = direction
                    lowest = value
            return output

class Room:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    @property
    def random_point(self):
        x = random.randint(self.x1, self.x2 -1)
        y = random.randint(self.y1, self.y2 -1)
        return maffs.Point(x, y)

    @property
    def centre(self):
        x = int((self.x1 + self.x2) / 2)
        y = int((self.y1 + self.y2) / 2)
        return maffs.Point(x, y)

    @property
    def cells(self):
        cells = []
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                cells.append([x, y])
        return cells

    def collide(self, other):
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1

def tunnel(x1, x2, y1, y2):
    if random.randint(0, 1) == 0:
        turn_x = x1
        turn_y = y2
    else:
        turn_x = x2
        turn_y = y1
    cells = [(turn_x, turn_y)]
    cells += [(turn_x, y) for y in range(min(y1, y2), max(y1,y2))]
    cells += [(x, turn_y) for x in range(min(x1, x2), max(x1,x2))]
    return cells

class EmptyLevel(Level):
    def generate(self):
        for x in range(self.size):
            for y in range(self.size):
                if x == 0 or x == self.size - 1 or y == 0 or y == self.size - 1:
                    self.add_entity(entities.make_wall(self, maffs.Point(x, y)))
                else:
                    self.add_entity(entities.make_floor(self, maffs.Point(x, y)))


class Dungeon(Level):
    def generate(self, maxRooms = 10):
        min_room_size = 3
        max_room_size = 7
        max_monsters_per_room = 5
        max_apples_per_room = 1
        int_map = []
        for x, row in enumerate(self.tiles):
            int_map.append([])
            for _ in row:
                int_map[x].append(1)
        baddies = []
        apples = []
        rooms = []
        fails_in_a_row = 0
        while len(rooms) < maxRooms and fails_in_a_row < 30:
            width = random.randint(min_room_size, max_room_size)
            x1 = random.randint(1, self.size - width - 1)
            x2 = x1 + width
            height = random.randint(min_room_size, max_room_size)
            y1 = random.randint(1, self.size - height - 1)
            y2 = y1 + height
            new_room = Room(x1, x2, y1, y2)
            new_room_valid = True
            for room in rooms:
                if room.collide(new_room):
                    new_room_valid = False
                    break
            if new_room_valid:
                fails_in_a_row = 0
                for cell in new_room.cells:
                    int_map[cell[0]][cell[1]] = 0
                num_monsters = random.randint(0, max_monsters_per_room) if len(rooms) > 1 else 0
                for _ in range(num_monsters):
                    point = new_room.random_point
                    while point in [(E.pos) for E in baddies]:
                        point = new_room.random_point
                    if random.randint(1, 3) == 3:
                        baddies.append(entities.make_goblin(self, point))
                    else:
                        baddies.append(entities.make_scorpion(self, point))
                num_apples = random.randint(0, max_apples_per_room)
                for _ in range(num_apples):
                    point = new_room.random_point
                    apples.append(entities.make_apple(self, point))
                if len(rooms) > 0:
                    # make a tunnel to the previous room
                    room_centre = new_room.random_point
                    last_centre = rooms[-1].random_point
                    x1 = room_centre.x
                    y1 = room_centre.y
                    x2 = last_centre.x
                    y2 = last_centre.y
                    for cell in tunnel(x1, x2, y1, y2):
                        int_map[cell[0]][cell[1]] = 0
                rooms.append(new_room)
            else:
                fails_in_a_row += 1

        self.start_pos = rooms[0].centre

        for x, row in enumerate(int_map):
            for y, cell in enumerate(row):
                if cell:
                    self.add_entity(entities.make_wall(self, maffs.Point(x, y)))
                else:
                    self.add_entity(entities.make_floor(self, maffs.Point(x, y)))
        self.add_entities(apples)
        self.add_entities(baddies)