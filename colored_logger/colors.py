#!/usr/bin/env python3

RESET = "\x1b[0m"  # reset

BLACK = "\x1b[30m"  # foreground black
RED = "\x1b[31m"  # foreground red
GREEN = "\x1b[32m"  # foreground green
YELLOW = "\x1b[33m"  # foreground yellow
BLUE = "\x1b[34m"  # foreground blue
MAGENTA = "\x1b[35m"  # foreground magenta
CYAN = "\x1b[36m"  # foreground cyan
WHITE = "\x1b[37m"  # foreground white

BLACK_BG = "\x1b[40m"  # bg black
RED_BG = "\x1b[41m"  # bg red
GREEN_BG = "\x1b[42m"  # bg green
YELLOW_BG = "\x1b[43m"  # bg yellow
BLUE_BG = "\x1b[44m"  # bg blue
MAGENTA_BG = "\x1b[45m"  # bg magenta
CYAN_BG = "\x1b[46m"  # bg cyan
WHITE_BG = "\x1b[47m"  # bg white

FOREGROUND_COLORS = {
    "": RESET,
    "BLACK": BLACK,
    "RED": RED,
    "GREEN": GREEN,
    "YELLOW": YELLOW,
    "BLUE": BLUE,
    "MAGENTA": MAGENTA,
    "CYAN": CYAN,
    "WHITE": WHITE,
}
BACKGROUND_COLORS = {
    "": RESET,
    "BLACK": BLACK_BG,
    "RED": RED_BG,
    "GREEN": GREEN_BG,
    "YELLOW": YELLOW_BG,
    "BLUE": BLUE_BG,
    "MAGENTA": MAGENTA_BG,
    "CYAN": CYAN_BG,
    "WHITE": WHITE_BG,
}

COLORS = {
    **FOREGROUND_COLORS,
    "BLACK-BG": BLACK_BG,
    "RED-BG": RED_BG,
    "GREEN-BG": GREEN_BG,
    "YELLOW-BG": YELLOW_BG,
    "BLUE-BG": BLUE_BG,
    "MAGENTA-BG": MAGENTA_BG,
    "CYAN-BG": CYAN_BG,
    "WHITE-BG": WHITE_BG,
}
