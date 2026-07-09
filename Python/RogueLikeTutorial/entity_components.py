import math
import maffs
import random
import log

actor_components = []

class EntityComponent:
    def __init__(self, owner):
        self.owner = owner
    
    @property
    def faction(self):
        return self.owner.faction

    @property
    def name(self):
        return self.owner.name
    
    @property
    def level(self):
        return self.owner.level
    
    @property
    def pos(self):
        return self.owner.pos
    
    @pos.setter
    def pos(self, new_pos):
        self.owner.pos = new_pos

class ActorComponent(EntityComponent):
    def __init__(self, owner, awake = False):
        self.owner = owner
        owner.actor_component = self
        self.awake = awake
        self.target_pos = None
        self.time_units = 0
        actor_components.append(self)

    @property
    def can_act(self):
        return self.awake and self.time_units > 0

    def die(self):
        actor_components.remove(self)

    def wake(self):
        log.log(f"The {self.name} wakes up!")
        self.awake = True
    
    def start_turn(self):
        if self.awake:
            self.time_units += 1.0

    def do_turn(self):
        while self.time_units > 0:
            self.do_stuff()

    def do_stuff(self):
        action = {'class': 'NPC', 'type': 'nothing'}
        self.level.scan_LOS(self.pos)
        targets = []
        target = None
        # scan for targets
        for other_entity in self.level.entities:
            if self.level.visible_map[other_entity.pos.x][other_entity.pos.y] and other_entity.faction != None and other_entity.faction != self.faction:
                targets.append(other_entity)
        # select a target
        if targets:
            closest = targets[0]
            distance = maffs.simple_distance(self.pos, targets[0].pos)
            for target in targets:
                if maffs.simple_distance(self.pos, target.pos) < distance:
                    distance = maffs.simple_distance(self.pos, target.pos)
                    closest = target
            self.target_pos = closest.pos
        # find path to target point
        if self.target_pos and self.pos != self.target_pos:
            direction = self.level.path_find(self.pos, self.target_pos)
            if direction:
                action = {'class': 'NPC', 'type': 'move', 'direction': direction}
        # kill the thing!
        distance = maffs.complex_distance(self.pos, self.target_pos)
        if target and distance == 1:
            action = {'class': 'NPC', 'type': 'attack', 'target': target}
        self.owner.unpack_action(action)

class PlayerMind(ActorComponent):
    action_buffer = None

    def die(self):
        log.log("Lol it looks like you died!")
        actor_components.remove(self)
    
    def do_turn(self):
        if self.action_buffer:
            self.owner.unpack_action(self.action_buffer)
        self.action_buffer = None

class MobilityComponent(EntityComponent):
    def __init__(self, owner, speed, modes = ["walk"]):
        self.owner = owner
        owner.mobility_component = self
        self.speed = speed
        self.active_mode = modes[0]
        self.modes = modes
    
    def add_mode(self, new_mode):
        self.modes.append(new_mode)
    
    def move(self, direction):
        TU_cost = math.sqrt(direction.x ** 2 + direction.y ** 2)
        mod_TU_cost = TU_cost / self.speed
        self.owner.actor_component.time_units -= mod_TU_cost
        new_pos = self.pos + direction
        if not self.level.is_cell_in_bounds(new_pos):
            return
        if self.level.is_passable_at(new_pos):
            self.level.move_entity(self.owner, new_pos)
            self.pos = new_pos

class CombatComponent(EntityComponent):
    def __init__(self, owner, hp: int, defense: int, power: int):
        self.owner = owner
        owner.combat_component = self
        self.max_hp = hp
        self._hp = hp
        self.defence = defense
        self.power = power

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = max(0, min(value, self.max_hp))

    def roll_melee_damage(self):
        return random.randint(1, 6) + self.power
    
    def take_damage(self, damage):
        mod_damage = max(0, damage - self.defence)
        self.hp -= mod_damage
        if self.hp == 0:
            self.owner.die()

    def heal(self, health):
        new_hp = min(self.hp + health, self.max_hp)
        delta = new_hp - self.hp
        self.hp = new_hp
        return delta

    def attack(self, target):
        self.owner.actor_component.time_units -= 1.0
        log.log(f"The {self.name} strikes the {target.name}!")
        if target.actor_component and not target.actor_component.awake:
            target.actor_component.wake()
        if target.combat_component:
            damage = self.roll_melee_damage()
            target.combat_component.take_damage(damage)

class InventoryComponent(EntityComponent):
    def __init__(self, owner, max_volume, items = []):
        self.owner = owner
        owner.inventory_component = self
        self.max_volume = max_volume
        self.items = []
        for item in items:
            self.insert(item)
        assert(self.total_volume <= self.max_volume)

    @property
    def total_mass(self):
        return sum([item.mass for item in self.items])

    @property
    def total_volume(self):
        return sum([item.volume for item in self.items])

    def insert(self, item):
        new_volume = self.total_volume + item.volume
        if new_volume <= self.max_volume:
            log.log(f"The {self.name} picks up the {item.name}!")
            self.items.append(item)
            return True
        else:
            log.log(f"There is no room for the {item.name} in the {self.name}!")
            return False

    def drop(self, item):
        if item in self.items:
            self.items.remove(item)
            item.pos = self.owner.pos
            self.owner.level.add_entity(item)
        else:
            print(f"The {item.name} is not in the {self.owner.name}'s inventory!")

    def grab_downwards(self):
        items = self.owner.level.get_grabbable_items_at(self.pos).copy()
        items.remove(self.owner)
        if items:
            item = items[-1]
            if self.insert(item):
                self.owner.level.remove_entity(item)
                item.pos = self.owner

class BodyComponent(EntityComponent):
    def __init__(self, owner, passable, transparent, mass, volume, rooted = False):
        self.owner = owner
        owner.body_component = self
        self.passable = passable
        self.transparent = transparent
        self.mass = mass
        self.volume = volume
        self.rooted = rooted

    @property
    def is_pickupable(self):
        return not self.rooted

class ActivationComponent(EntityComponent):
    def __init__(self, owner):
        self.owner = owner
        owner.activation_component = self
    
    def activate(self, actor):
        log.log("Default item activation")

class EdibleComponent(ActivationComponent):
    def activate(self, actor):
        log.log(f"The {actor.name} eats the {self.owner.name}")
        actor.combat_component.heal(random.randint(5, 15))
        self.owner.destroy()