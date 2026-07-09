UI_panel_characters_width = 30

log_entries = []
raw_log = []

def log(entry):
    raw_log.append(entry)
    if len(entry) < UI_panel_characters_width - 5:
        log_entries.append(f">>> {entry}")
    else:
        lines = []
        words = entry.split(" ")
        line = ">>>"
        for word in words:
            while len(word) > UI_panel_characters_width - 1:
                if len(line) == UI_panel_characters_width -1:
                    lines.append(line)
                    line = ""
                space_left = (UI_panel_characters_width - 2) - (len(line) + 1)
                if line:
                    line += " " + word[0:space_left] + "-"
                else:
                    space_left += 1
                    line += word[0:space_left] + "-"
                lines.append(line)
                line = ""
                word = word[space_left:]
            if len(line + " " + word) > UI_panel_characters_width - 1:
                lines.append(line)
                line = word
            elif line:
                line += " " + word
            else:
                line += word
        lines.append(line)
        for line in lines.__reversed__():
            log_entries.append(line)
