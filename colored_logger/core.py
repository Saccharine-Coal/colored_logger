from __future__ import annotations
import logging

import colored_logger.colors as colors
import colored_logger.symbols as symbols


class CustomFormatter(logging.Formatter):
    RESET = "\x1b[0m"  # reset
    BLACK = "\x1b[30m"  # foreground black
    RED = "\x1b[31m"  # foreground red
    GREEN = "\x1b[32m"  # foreground green
    YELLOW = "\x1b[33m"  # foreground yellow
    BLUE = "\x1b[34m"  # foreground blue
    MAGENTA = "\x1b[35m"  # foreground magenta
    CYAN = "\x1b[36m"  # foreground cyan
    WHITE = "\x1b[37m"  # foreground white

    def __init__(
        self,
        name,
        print_colors=False,
        endcap="triangle-filled",
        print_arrows=False,
        connector_color: str = "",
        print_dict=False,
        level: str = "WARN",
        shortend_names=True,
        **formatter_kwargs,
    ):
        super().__init__(**formatter_kwargs)
        # https://www.w3.org/TR/xml-entity-names/025.html
        self.STR_TO_COLOR = colors.COLORS
        self.INT_TO_STR: dict[int, str] = {
            0: "",
            logging.DEBUG: "MAGENTA",
            logging.INFO: "GREEN",
            logging.WARNING: "YELLOW",
            logging.ERROR: "RED",
            logging.CRITICAL: "RED",
        }
        self.ENDCAPS = symbols.ENDCAPS
        self.CONNECTORS = symbols.CONNECTORS
        level = level.upper()  # convert lowercase to uppercase
        STR_TO_LOGLEVEL = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARN,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        _SHORT_NAMES = {
            "DEBUG": "DBUG",
            "INFO": "INFO",
            "WARN": "WARN",
            "ERROR": "ERRR",
            "CRITICAL": "CRIT",
        }
        self.shortend_names = shortend_names
        self.startcap = self.ENDCAPS["square-filled"]
        if self.shortend_names:
            for key, val in STR_TO_LOGLEVEL.items():
                logging.addLevelName(val, _SHORT_NAMES[key])
        self.name = name
        self.level = level
        self.endcap = endcap
        self.connector = "double"
        self.connector_color = self.STR_TO_COLOR[connector_color.upper()]
        self.msg_length = 6
        self.msg_hspace = 1
        self.msg_tab = self.msg_length + 1 + self.msg_hspace
        self.num_tabs = 15
        if print_colors:
            print("BLACK:\t\t" + self.BLACK + "HELLO" + self.RESET)
            print("RED:\t\t" + self.RED + "HELLO" + self.RESET)
            print("GREEN:\t\t" + self.GREEN + "HELLO" + self.RESET)
            print("YELLOW:\t\t" + self.YELLOW + "HELLO" + self.RESET)
            print("BLUE:\t\t" + self.BLUE + "HELLO" + self.RESET)
            print("MAGENTA:\t" + self.MAGENTA + "HELLO" + self.RESET)
            print("CYAN:\t\t" + self.CYAN + "HELLO" + self.RESET)
            print("WHITE:\t\t" + self.WHITE + "HELLO" + self.RESET)
        if print_arrows:
            print(self.connector_color + "\u2560\u2550\u25b6")
            print("\u2560\u2550\u25b7")
            print("\u2560\u2550\u25c7" + self.RESET)
        if print_dict:
            print(self.ENDCAPS)
            print(self.CONNECTORS)
            bg = {
                "BLACK-BG": "\x1b[40m",  # foreground black
                "RED-BG": "\x1b[41m",  # foreground red
                "GREEN-BG": "\x1b[42m",  # foreground green
                "YELLOW-BG": "\x1b[43m",  # foreground yellow
                "BLUE-BG": "\x1b[44m",  # foreground blue
                "MAGENTA-BG": "\x1b[45m",  # foreground magenta
                "CYAN-BG": "\x1b[46m",  # foreground cyan
                "WHITE-BG": "\x1b[47m",  # foreground whit
            }
            for key in bg.keys():
                print(bg[key] + self.BLACK + f"  {key}  ", self.RESET)
        print(self.STR_TO_COLOR["CYAN-BG"] + self.BLACK + f" {name} " + self.RESET)
        print(symbols.CONNECTORS[self.connector]["vertical"])

    def _get_endcap(self, right=True) -> str:
        fmt = ""
        if self.endcap == "triangle-filled" or self.endcap == "triangle":
            if right:
                fmt = self.ENDCAPS["right-" + self.endcap]
            else:
                fmt = self.ENDCAPS["left-" + self.endcap]
                fmt = self.startcap
        elif self.endcap in self.ENDCAPS.keys():
            fmt = self.ENDCAPS[self.endcap]
        else:
            raise ValueError
        return fmt + " " * self.msg_hspace

    def _get_arrow(self, length=1, right=True, endcap_color="") -> str:
        connectors = self.CONNECTORS[self.connector]
        fmt = self.connector_color
        fmt += connectors["vertical-and-right"]
        fmt += connectors["horizontal"] * length
        # fmt += (
        #     self.STR_TO_COLOR[endcap_color.upper()] if endcap_color else ""
        # ) + self._get_endcap(right=right)
        fmt += endcap_color + self._get_endcap(right=right)
        fmt += self.RESET
        return fmt

    def _get_color(self, input, bg=False) -> str:
        def as_color_code(input_str: str, bg: bool) -> str:
            color_code = ""
            for color in input_str.split(","):
                if bg:
                    color += "-bg"
                color_code += self.STR_TO_COLOR[color.upper()]
            return color_code

        if isinstance(input, int):
            return as_color_code(self.INT_TO_STR[input], bg)
        else:
            return as_color_code(input, bg)

    def _get_format(self, levelno: int) -> str:
        level_fmt = f"{self._get_arrow(length=0, right=False, endcap_color=self._get_color(levelno))}{self._get_color(levelno, bg=levelno == logging.CRITICAL)}%(levelname)s{self.RESET}:"
        header_fmt = (
            ("\t" * self.num_tabs)
            + f"{self.RESET}{self.CYAN}%(module)s.%(funcName)s():%(lineno)d{self.RESET}\n"
        )

        connector_fmt = self._get_arrow(
            length=self.msg_length, endcap_color=self._get_color(levelno)
        )
        message_fmt = "%(message)s" + self.RESET
        NAME = ""
        FORMATS: dict[int, str] = {
            logging.DEBUG: header_fmt + connector_fmt + message_fmt,
            logging.INFO: NAME
            + self._get_color(levelno)
            + header_fmt
            + connector_fmt
            + message_fmt,
            logging.WARNING: NAME
            + self._get_color(levelno)
            + header_fmt
            + connector_fmt
            + message_fmt,
            logging.ERROR: NAME
            + self._get_color(levelno)
            + header_fmt
            + connector_fmt
            + message_fmt,
            logging.CRITICAL: NAME
            + self._get_color(levelno)
            + header_fmt
            + connector_fmt
            + message_fmt,
        }
        return level_fmt + FORMATS[levelno]

    def format(self, record):
        log_fmt = self._get_format(record.levelno)
        formatter = logging.Formatter(log_fmt)
        if "\n" in record.msg:  # insert decorations to message
            msg = ""
            for i, line in enumerate(record.msg.splitlines()):
                if i != 0:
                    msg += (
                        "\n"
                        + self.connector_color
                        + self.CONNECTORS[self.connector]["vertical"]
                        + self.RESET
                        + " " * self.msg_tab
                    )
                msg += line
            record.msg = msg
        fmt = formatter.format(record)
        if "<module>()" in fmt:  # remove <module>
            fmt = fmt.replace(".<module>()", "")
        return fmt


def get_logger(formatter: CustomFormatter) -> logging.Logger:
    name, level = formatter.name, formatter.level
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
