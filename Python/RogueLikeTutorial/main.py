import pygame
import entities
import renderer
import levels
import log
import interface

frames = 0
total_frame_time = 0
def measure_performance(frame_time):
    global frames
    global total_frame_time
    frames += 1
    total_frame_time += frame_time

def show_performance():
    global frames
    global total_frame_time
    if frames == 0:
        frames = 1
    avg_frame_time = total_frame_time / frames
    print(f"Avg. ms/f: {avg_frame_time:.2f}, Frames: {frames}")
    frames = 0
    total_frame_time = 0

def process_system_action(action):
    if action['type'] == 'escape':
        if interface.panels:
            interface.panels[-1].queue_close()
        else:
            pygame.quit()
            quit()
    if action['type'] == 'inventory':
        interface.panels.append(interface.Inventory(player.inventory_component.items, "Inventory"))

active_level = levels.Dungeon(renderer.level_size)

active_level.generate()

player = entities.Entity(active_level, active_level.start_pos, "player", "player", "player_faction")
entities.BodyComponent(player, False, True, 1, 1, False)
entities.MobilityComponent(player, 1.0)
entities.PlayerMind(player, True)
entities.CombatComponent(player, 20, 0, 0)
entities.InventoryComponent(player, 8, [entities.make_apple(active_level, player), entities.make_skull(active_level, player)])
active_level.add_entity(player)

log.log("It's dungeon time!")

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # if event.type == pygame.USEREVENT:
            # show_performance()
        if event.type == pygame.KEYDOWN:
            action = interface.handle_input(event.key)
            if action['class'] is None:
                continue
            if action['class'] == 'interface':
                action = interface.panels[-1].process_action(action)
                if action == None:
                    continue
            if action['class'] == 'player':
                player.actor_component.action_buffer = action
            if action['class'] == 'system':
                process_system_action(action)
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     point = input_handlers.handle_mouse_click(event)
        #     step = active_level.path_find(player.pos, point)
        #     if step:
        #         action = {'class': None, 'type': None}
        #         action['class'] = 'player'
        #         action['type'] = 'move'
        #         action['direction'] = step
        #         player.actor_component.action_buffer = action
        # if event.type == pygame.MOUSEMOTION:
        #     input_handlers.handle_mouse_motion(event)
    interface.panels = [panel for panel in interface.panels if not panel.flag_close]
    active_level.handle_turns()
    active_level.scan_LOS(player.pos)
    renderer.render(active_level, player)
    # measure_performance(clock.get_rawtime())
    clock.tick(30)