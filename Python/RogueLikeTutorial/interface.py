import pygame
import maffs
import renderer

panels = []

def handle_input(key):
    if panels:
        return handle_interface_input(key)
    else:
        return handle_action_input(key)

def handle_action_input(key):
    action = {'class': None, 'type': None}
    if key == pygame.K_UP or key == pygame.K_KP8:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(y = -1)
    elif key == pygame.K_DOWN or key == pygame.K_KP2:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(y = 1)
    elif key == pygame.K_LEFT or key == pygame.K_KP4:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(x = -1)
    elif key == pygame.K_RIGHT or key == pygame.K_KP6:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(x = 1)
    elif key == pygame.K_KP7:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(x = -1, y = -1)
    elif key == pygame.K_KP9:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(x = 1, y = -1)
    elif key == pygame.K_KP1:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(x = -1, y = 1)
    elif key == pygame.K_KP3:
        action['class'] = 'player'
        action['type'] = "bump"
        action['direction'] = maffs.Point(x = 1, y = 1)
    elif key == pygame.K_g:
        action['class'] = 'player'
        action['type'] = 'grab'
    elif key == pygame.K_i:
        action['class'] = 'system'
        action['type'] = 'inventory'
    elif key == pygame.K_KP5:
        action['class'] = 'player'
        action['type'] = 'nothing'
    elif key == pygame.K_ESCAPE:
        action['class'] = 'system'
        action['type'] = 'escape'
    return action

def handle_interface_input(key):
    action = {'class': None, 'type': None}
    if key == pygame.K_UP:
        action['class'] = 'interface'
        action['type'] = "up"
    elif key == pygame.K_DOWN:
        action['class'] = 'interface'
        action['type'] = "down"
    elif key == pygame.K_LEFT:
        action['class'] = 'interface'
        action['type'] = "left"
    elif key == pygame.K_RIGHT:
        action['class'] = 'interface'
        action['type'] = "right"
    elif key == pygame.K_1 or key == pygame.K_KP_1:
        action['class'] = 'interface'
        action['type'] = "1"
    elif key == pygame.K_2 or key == pygame.K_KP_2:
        action['class'] = 'interface'
        action['type'] = "2"
    elif key == pygame.K_3 or key == pygame.K_KP_3:
        action['class'] = 'interface'
        action['type'] = "3"
    elif key == pygame.K_4 or key == pygame.K_KP_4:
        action['class'] = 'interface'
        action['type'] = "4"
    elif key == pygame.K_5 or key == pygame.K_KP_5:
        action['class'] = 'interface'
        action['type'] = "5"
    elif key == pygame.K_6 or key == pygame.K_KP_6:
        action['class'] = 'interface'
        action['type'] = "6"
    elif key == pygame.K_7 or key == pygame.K_KP_7:
        action['class'] = 'interface'
        action['type'] = "7"
    elif key == pygame.K_8 or key == pygame.K_KP_8:
        action['class'] = 'interface'
        action['type'] = "8"
    elif key == pygame.K_9 or key == pygame.K_KP_9:
        action['class'] = 'interface'
        action['type'] = "9"
    elif key == pygame.K_0 or key == pygame.K_KP_0:
        action['class'] = 'interface'
        action['type'] = "0"
    elif key == pygame.K_SPACE:
        action['class'] = 'interface'
        action['type'] = "enter"
    elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
        action['class'] = 'interface'
        action['type'] = "enter"
    elif key == pygame.K_i:
        action['class'] = 'system'
        action['type'] = 'escape'
    elif key == pygame.K_ESCAPE:
        action['class'] = 'system'
        action['type'] = 'escape'
    return action

def handle_mouse_click(input):
    return maffs.Point(int(input.pos[0]/renderer.grid_size), int(input.pos[1]/renderer.grid_size))

def handle_mouse_motion(input):
    print("Zoom!", input.pos, input.rel, input.buttons)

class Button:
    def __init__(self, function):
        self.function = function
    
    def execute(self):
        self.function()

class Panel:
    flag_close = False

    def queue_close(self):
        self.flag_close = True
    
    def get_lines(self):
        lines = []
        lines.append("┌───────┐")
        lines.append("│Default│")
        lines.append("└───────┘")
        return lines

    def process_action(self, action):
        print("Default interface process")
        print(action)

class Popup(Panel):
    def __init__(self, message, title = "Information:"):
        self.message = message
        self.title = title
    
    def get_lines(self):
        width = max(len(self.message), len(self.title))
        lines = []
        lines.append("┌" + "─"*width + "┐")
        lines.append("│" + self.title.ljust(width) + "│")
        lines.append("│" + self.message.ljust(width) + "│")
        lines.append("└" + "─"*width + "┘")
        return lines

    def process_action(self, action):
        if action['type'] == 'enter' or action['type'] == 'escape':
            self.queue_close()

class ItemViewer(Panel):
    def __init__(self, item):
        self.item = item
    
    def get_lines(self):
        width = len("Do what with your " + self.item.name + "?")
        lines = []
        lines.append("┌" + "─"*width + "┐")
        lines.append("│" + self.item.name.ljust(width) + "│")
        lines.append(("│Mass:" + str(self.item.mass)).ljust(width+1) + "│")
        lines.append(("│Size:" + str(self.item.volume)).ljust(width+1) + "│")
        lines.append("│Do what with your " + self.item.name + "?│")
        lines.append("│1) Drop it".ljust(width+1) + "│")
        lines.append("│2) Use it".ljust(width+1) + "│")
        lines.append("│3) Cancel".ljust(width+1) + "│")
        lines.append("└" + "─"*width + "┘")
        return lines

    def process_action(self, action):
        new_action = {'class': 'player', 'object': self.item}
        if action['type'] == 'enter' or action['type'] == 'escape':
            self.queue_close()
            return None
        elif action['type'] == '1':
            self.queue_close()
            new_action['type'] = 'drop'
        elif action['type'] == '2':
            self.queue_close()
            new_action['type'] = 'activate'
        elif action['type'] == '3':
            self.queue_close()
            return None
        return new_action


class SelectionMenu(Panel):
    def __init__(self, choices, title = "Choose wisely!", selection = 0):
        self.title = title
        self.selection = selection
        self.current_index = 0
        self.choices = choices
        # self.last_element = min(10, len(choices))
        # if len(choices) > 10:
        #     self.pages = [choices[x:x+9] for x in range(0, len(choices), 9)]
        #     for i, page in enumerate(self.pages):
        #         page_turner = Action(f"More →| ({i+1}//{len(self.pages)})", self.next_page)
        #         page.append(page_turner)
        # else:
        #     self.pages = [choices]
        # self.current_page = self.pages[0]
    
    def get_lines(self):
        width = max(len(self.title), max(map(len, self.choices)) + 3)
        lines = []
        lines.append(f"┌{'─' * width}┐")
        lines.append(f"│{self.title.ljust(width)}│")
        lines.append(f"├{'─' * (width - 2)}┬─┤")
        for y, choice in enumerate(self.choices):
            cursor = '>' if y == self.selection else " "
            index = y + 1
            if y == self.selection:
                index = "<"
            elif y == self.selection + 1:
                index = "↓"
            elif y == self.selection - 1:
                index = "↑"
            lines.append(f"│{cursor}{choice.ljust(width - 3)}│{index}│")
        lines.append(f"└{'─' * (width - 2)}┴─┘")
        return lines
    
    def select(self):
        self.queue_close()
        selection = self.choices[self.selection]
        return selection

    def process_action(self, action):
        if action["type"].isnumeric():
            if self.selection == int(action["type"]) - 1:
                self.select()
            self.selection = int(action["type"]) - 1
        elif action["type"] == "up":
            self.selection -= 1
        elif action["type"] == "down":
            self.selection += 1
        elif action['type'] == 'enter':
            self.select()
        if self.selection == -1:
            self.selection = len(self.choices) - 1
        if self.selection >= len(self.choices):
            self.selection = 0

class Inventory(SelectionMenu):    
    def get_lines(self):
        if not self.choices:
            entries = ["empty"]
        else:
            entries = [str(item) for item in self.choices]
        width = max(len(self.title), max(map(len, entries)) + 3)
        lines = []
        lines.append(f"┌{'─' * width}┐")
        lines.append(f"│{self.title.ljust(width)}│")
        lines.append(f"├{'─' * (width - 2)}┬─┤")
        for y, choice in enumerate(entries):
            cursor = '>' if y == self.selection else " "
            index = y + 1
            if y == self.selection:
                index = "<"
            elif y == self.selection + 1:
                index = "↓"
            elif y == self.selection - 1:
                index = "↑"
            lines.append(f"│{cursor}{choice.ljust(width - 3)}│{index}│")
        lines.append(f"└{'─' * (width - 2)}┴─┘")
        return lines
    
    def select(self):
        self.queue_close()
        if self.choices:
            selection = self.choices[self.selection]
            viewer = ItemViewer(selection)
            panels.append(viewer)

    
    # def process_key_input(self, event):
    #     # returns True if the player has taken an action
    #     if event.key == pygame.K_ESCAPE:
    #         self.flag_close = True
    #     elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
    #         if self.current_page[self.selection].callable == self.next_page:
    #             self.next_page()
    #         else:
    #             self.current_page[self.selection].callable()
    #             self.flag_close = True
    #             return True
    #     elif event.key == pygame.K_UP:
    #         if self.selection == 0:
    #             self.selection = self.last_element -1
    #         else:
    #             self.selection -= 1
    #         self.make_graphic()
    #     elif event.key == pygame.K_DOWN:
    #         if self.selection == self.last_element -1:
    #             self.selection = 0
    #         else:
    #             self.selection += 1
    #         self.make_graphic()
    #     elif event.unicode.isnumeric():
    #         number = int(event.unicode)
    #         if number == 0:
    #             number = 10
    #         if number > self.last_element:
    #             return False
    #         if number - 1 == self.selection:
    #             if self.current_page[self.selection].callable == self.next_page:
    #                 self.next_page()
    #             else:
    #                 self.current_page[self.selection].callable()
    #                 self.flag_close = True
    #                 return True
    #         else:
    #             self.selection = number - 1
    #             self.make_graphic()
    #     elif event.key == pygame.K_TAB:
    #         self.next_page()
    #     else:
    #         return False

    # def next_page(self):
    #     self.current_index += 1
    #     if self.current_index >= len(self.pages):
    #         self.current_index = 0
    #     self.make_graphic()
    #     if self.selection > self.last_element:
    #         self.selection = 0
    #         self.make_graphic()

    # def make_graphic(self):
    #     longest = 1
    #     for choice in self.current_page:
    #         if len(choice.description) > longest:
    #             longest = len(choice.description)
    #     total_width = max(longest + 3, len(self.prompt)) + 2
    #     total_height = len(self.current_page) + 4
    #     # if self.pages == 1:
    #     #     total_height = len(self.choices) + 4
    #     # elif self.current_page == self.pages -1:
    #     #     total_height = len(self.choices) % 10 + 4
    #     # else:
    #     #     total_height = 14
    #     self.last_element = total_height - 4
    #     char_w, char_h = self.font.size("A")
    #     width = char_w * total_width
    #     height = char_h * total_height
    #     self.rect = pygame.rect.Rect(- width / 2, - height / 2, width, height)
    #     self.graphic = pygame.Surface((width, height))
    #     self.graphic.fill(UI_BG_colour)
    #     lines = []
    #     lines.append(f"╔{'═' * (total_width - 2)}╗")
    #     lines.append(f"║{self.prompt.ljust(total_width - 2)}║")
    #     lines.append(f"╟{'─' * (total_width - 4)}┬─╢")
    #     for y, choice in enumerate(self.current_page):
    #         cursor = '>' if y == self.selection else "-"
    #         index = y + 1 if y != 9 else 0
    #         if y == self.selection:
    #             index = "<"
    #         elif y == self.selection + 1:
    #             index = "↓"
    #         elif y == self.selection - 1:
    #             index = "↑"
    #         lines.append(f"║{cursor}{choice.description.ljust(total_width - 5)}│{index}║")
    #     lines.append(f"╚{'═' * (total_width - 4)}╧═╝")
    #     for y, line in enumerate(lines):
    #         self.graphic.blit(self.font.render(line, False, UI_text_colour), (0, char_h * y))