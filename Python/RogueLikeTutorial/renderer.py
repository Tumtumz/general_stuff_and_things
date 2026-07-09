import pygame
import levels
import log
import interface

level_size = 30
grid_size = 32
UI_gridsize = 16
white  = (255, 255, 255)
black  = (  0,   0,   0)
grey   = (128, 128, 128)
red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
cyan   = (  0, 255, 255)
pink   = (255,   0, 255)
yellow = (255, 255,   0)

window_size = grid_size * level_size
ui_panel_width = UI_gridsize * level_size

pygame.init()
font = pygame.font.Font("FreeMono.ttf", grid_size)
window = pygame.display.set_mode((window_size + ui_panel_width, window_size))
fog_of_war = pygame.Surface((window_size, window_size))
pygame.display.set_caption("RogueLikeTutorial")

def get_from_tilesheet(tilesheet, x, y, offset, tile_size, transparent = False, grid_size = grid_size):
    surface = pygame.Surface((tile_size, tile_size))
    surface.blit(tilesheet, (0, 0), (x * (tile_size + offset), y * (tile_size + offset), tile_size, tile_size))
    surface = pygame.transform.scale(surface, (grid_size, grid_size))
    if transparent:
        surface.set_colorkey(black)
    return surface

def CharacterGraphic(character, colour, highlight, background, circle = True):
    surface = pygame.Surface((grid_size, grid_size), pygame.SRCALPHA)
    if circle:
        pygame.draw.circle(surface, background, (grid_size/2, grid_size/2), grid_size/2)
    else:
        surface.fill(background)
    surface.blit(font.render(character, False, highlight), (grid_size/4, 0))
    surface.blit(font.render(character, False, colour), (grid_size/4 + 1, 1))
    return surface

def grayscale(img, brightness = 1.0):
    arr = pygame.surfarray.array3d(img)
    arr = arr.dot([0.298 * brightness, 0.587 * brightness, 0.114 * brightness])[:,:,None].repeat(3,axis=2)
    return pygame.surfarray.make_surface(arr)

def render(level: levels.Level, player):
    window.fill(black)
    window.blit(fog_of_war, (0, 0))
    for x, row in enumerate(level.tiles):
        for y, cell in enumerate(row):
            cell_graphic = pygame.Surface((grid_size, grid_size))
            cell_rect = (x * grid_size, y * grid_size)
            if level.visible_map[x][y]:
                for entity in cell:
                    cell_graphic.blit(graphics[entity.graphic_ID], (0, 0))
                window.blit(cell_graphic, cell_rect)
                grey_image = grayscale(cell_graphic, 0.5)
                fog_of_war.blit(grey_image, (entity.pos.x * grid_size, entity.pos.y * grid_size))
    draw_dashboard(player)
    for panel in interface.panels:
        draw_panel(panel)
    pygame.display.update()

def draw_panel(panel):
    lines = panel.get_lines()
    height = len(lines)
    width = max(map(len, lines))
    surface = pygame.Surface((width * UI_gridsize, height * UI_gridsize))
    for i, line in enumerate(lines):
        surface.blit(render_text(line), (0, i * UI_gridsize))
    window.blit(surface, (0, 0))

def draw_dashboard(player):
    rect = pygame.Rect(window_size, 0, ui_panel_width, window_size)
    surface = pygame.Surface((ui_panel_width, window_size))
    lines = ["│".ljust(level_size) for _ in range(level_size * 2)]
    space_for_log = 15
    lines[0] = f"│Player is dead...".ljust(level_size)
    if player.is_alive:
        lines[0] = f"│Player HP: {player.combat_component.hp}%{player.combat_component.max_hp}".ljust(level_size)
        lines[1] = "│" + ("♥"*player.combat_component.hp).ljust(player.combat_component.max_hp, "♡").ljust(level_size)
    else:
        lines[1] = "│☠".ljust(level_size)
    lines[-(space_for_log + 1)] = "├".ljust(level_size,"─")
    for i, entry in enumerate(log.log_entries[-space_for_log:].__reversed__()):
        lines[i - space_for_log] = "│" + entry.ljust(level_size)
        # surface.blit(render_text(entry), (UI_gridsize, ((level_size * 2) - space_for_log + i) *  UI_gridsize))
    for i, line in enumerate(lines):
        surface.blit(render_text(line), (0, i * UI_gridsize)) 
    window.blit(surface, rect)

def render_text(string: str):
    string = string.upper()
    surface = pygame.Surface((UI_gridsize * len(string), UI_gridsize))
    for i, character in enumerate(string):
        surface.blit(UI_graphics[character], (i * UI_gridsize, 0))
    return surface

graphics = {}

tileset = pygame.image.load("colored_packed.png")
tileset_transparent = pygame.image.load("colored-transparent_packed.png")

graphics["default"] = CharacterGraphic("?", red, pink, black)
graphics["player"] = get_from_tilesheet(tileset_transparent, 25, 0, 0, 16, True)
graphics["wizard"] = get_from_tilesheet(tileset_transparent, 24, 1, 0, 16, True)
graphics["goblin"] = get_from_tilesheet(tileset_transparent, 25, 2, 0, 16, True)
graphics["scorpion"] = get_from_tilesheet(tileset_transparent, 24, 5, 0, 16, True)
graphics["corpse"] = get_from_tilesheet(tileset_transparent, 0, 15, 0, 16, True)
graphics["apple"] = get_from_tilesheet(tileset_transparent, 33, 18, 0, 16, True)
graphics["skull"] = get_from_tilesheet(tileset_transparent, 34, 12, 0, 16, True)
graphics["wall"] = get_from_tilesheet(tileset, 10, 17, 0, 16)
graphics["floor"] = get_from_tilesheet(tileset, 2, 0, 0, 16)

UI_graphics = {}
sprite_coords = []
# numbers row
for x, letter in enumerate("0123456789:.%"):
    UI_graphics[letter] = get_from_tilesheet(tileset, x + 35, 17, 0, 16, grid_size = UI_gridsize)
# letters row 1
for x, letter in enumerate("ABCDEFGHIJKLM"):
    UI_graphics[letter] = get_from_tilesheet(tileset, x + 35, 18, 0, 16, grid_size = UI_gridsize)
# letters row 2
for x, letter in enumerate("NOPQRSTUVWXYZ"):
    UI_graphics[letter] = get_from_tilesheet(tileset, x + 35, 19, 0, 16, grid_size = UI_gridsize)
# specials row
for x, letter in enumerate("#+-*/=@"):
    UI_graphics[letter] = get_from_tilesheet(tileset, x + 35, 20, 0, 16, grid_size = UI_gridsize)

UI_graphics["corpse"] = get_from_tilesheet(tileset_transparent, 0, 15, 0, 16, True, grid_size = UI_gridsize)
UI_graphics["apple"] = get_from_tilesheet(tileset_transparent, 33, 18, 0, 16, True, grid_size = UI_gridsize)

UI_graphics[" "] = get_from_tilesheet(tileset, 0, 0, 0, 16, grid_size = UI_gridsize)
UI_graphics[","] = get_from_tilesheet(tileset, 0, 0, 0, 16, grid_size = UI_gridsize)
UI_graphics["!"] = get_from_tilesheet(tileset, 35, 13, 0, 16, grid_size = UI_gridsize)
UI_graphics["?"] = get_from_tilesheet(tileset, 37, 13, 0, 16, grid_size = UI_gridsize)
UI_graphics[">"] = get_from_tilesheet(tileset, 24, 20, 0, 16, grid_size = UI_gridsize)
UI_graphics["<"] = get_from_tilesheet(tileset, 26, 20, 0, 16, grid_size = UI_gridsize)
UI_graphics["("] = get_from_tilesheet(tileset, 26, 20, 0, 16, grid_size = UI_gridsize)
UI_graphics[")"] = get_from_tilesheet(tileset, 24, 20, 0, 16, grid_size = UI_gridsize)
UI_graphics["↓"] = get_from_tilesheet(tileset, 25, 20, 0, 16, grid_size = UI_gridsize)
UI_graphics["↑"] = get_from_tilesheet(tileset, 23, 20, 0, 16, grid_size = UI_gridsize)

UI_graphics["♡"] = get_from_tilesheet(tileset, 40, 10, 0, 16, grid_size = UI_gridsize)
UI_graphics["♥"] = get_from_tilesheet(tileset, 42, 10, 0, 16, grid_size = UI_gridsize)
UI_graphics["☠"] = get_from_tilesheet(tileset, 34, 12, 0, 16, grid_size = UI_gridsize)

UI_graphics["'"] = pygame.transform.rotate(UI_graphics["."], 180)
# ┼
UI_graphics["┼"] = get_from_tilesheet(tileset, 16, 3, 0, 16, grid_size = UI_gridsize)
# │
UI_graphics["│"] = get_from_tilesheet(tileset, 14, 3, 0, 16, grid_size = UI_gridsize)
# ─
UI_graphics["─"] = pygame.transform.rotate(UI_graphics["│"], 90)
# ┌
UI_graphics["┌"] = get_from_tilesheet(tileset, 15, 3, 0, 16, grid_size = UI_gridsize)
# ┐
UI_graphics["┐"] = pygame.transform.rotate(UI_graphics["┌"], 270)
# ┘
UI_graphics["┘"] = pygame.transform.rotate(UI_graphics["┌"], 180)
# └
UI_graphics["└"] = pygame.transform.rotate(UI_graphics["┌"], 90)
# ├
UI_graphics["├"] = get_from_tilesheet(tileset, 17, 3, 0, 16, grid_size = UI_gridsize)
# ┬
UI_graphics["┬"] = pygame.transform.rotate(UI_graphics["├"], 270)
# ┤
UI_graphics["┤"] = pygame.transform.rotate(UI_graphics["├"], 180)
# ┴
UI_graphics["┴"] = pygame.transform.rotate(UI_graphics["├"], 90)
