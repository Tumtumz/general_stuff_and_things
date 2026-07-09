from entity_components import *
import log

class Entity:
    def __init__(self, level, pos, name = "nameless entity", graphic_ID = "default", faction = None):
        self.level = level
        self.pos = pos
        self.name = name
        self.graphic_ID = graphic_ID
        self.faction = faction
        self.body_component = None
        self.mobility_component = None
        self.actor_component = None
        self.combat_component = None
        self.inventory_component = None
        self.activation_component = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"entity: {self.name}, location: {self.pos}"

    @property
    def transparent(self):
        return self.body_component.transparent

    @property
    def passable(self):
        return self.body_component.passable

    @property
    def mass(self):
        return self.body_component.mass
    
    @property
    def volume(self):
        return self.body_component.volume
    
    @property
    def rooted(self):
        return self.body_component.rooted

    def die(self):
        log.log(f"The {self.name} dies!")
        self.actor_component.die()
        self.mobility_component = None
        self.combat_component = None
        self.faction = None
        self.body_component.passable = True
        self.name = "dead " + self.name
        self.graphic_ID = "corpse"
        EdibleComponent(self)

    def unpack_action(self, action):
        if action['type'] == 'bump':
            new_pos = self.pos + action['direction']
            if self.level.is_passable_at(new_pos):
                self.mobility_component.move(action['direction'])
            else:
                blocker = self.level.get_blocking_entity_at(new_pos)
                self.combat_component.attack(blocker)
        elif action['type'] == 'move':
            self.mobility_component.move(action['direction'])
        elif action['type'] == 'attack':
            self.combat_component.attack(action['target'])
        elif action['type'] == 'grab':
            self.inventory_component.grab_downwards()
        elif action['type'] == 'drop':
            self.inventory_component.drop(action['object'])
        elif action['type'] == 'activate':
            if action['object'].activation_component:
                action['object'].activation_component.activate(self)
            else:
                log.log(f"You can't do anything interesting with this {action['object'].name}")
        elif action['type'] == 'nothing':
            self.actor_component.time_units = min(0.0, self.actor_component.time_units)
        else:
            log.log(f"Not yet implemented action type: {action['type']}")

    @property
    def is_alive(self):
        return self.combat_component != None and self.combat_component.hp != 0
    
    def destroy(self):
        if type(self.pos) == Entity:
            self.pos.inventory_component.drop(self)
        self.level.remove_entity(self)

def make_apple(level, pos):
    apple = Entity(level, pos, "apple", "apple")
    BodyComponent(apple, True, True, 1, 1, False)
    EdibleComponent(apple)
    return apple

def make_skull(level, pos):
    skull = Entity(level, pos, "skull", "skull")
    BodyComponent(skull, True, True, 1, 1, False)
    return skull

def make_goblin(level, pos):
    goblin = Entity(level, pos, "goblin", "goblin", "baddies_faction")
    BodyComponent(goblin, False, True, 1, 1)
    MobilityComponent(goblin, 0.9)
    ActorComponent(goblin)
    CombatComponent(goblin, 10, 1, 1)
    return goblin

def make_scorpion(level, pos):
    scorpion = Entity(level, pos, "scorpion", "scorpion", "baddies_faction")
    BodyComponent(scorpion, False, True, 1, 1)
    MobilityComponent(scorpion, 0.8)
    ActorComponent(scorpion)
    CombatComponent(scorpion, 6, 2, 3)
    return scorpion

def make_wall(level, pos):
    wall = Entity(level, pos, "wall", "wall", None)
    BodyComponent(wall, False, False, 1, 1, True)
    return wall

def make_floor(level, pos):
    floor = Entity(level, pos, "floor", "floor")
    BodyComponent(floor, True, True, 1, 1, True)
    return floor