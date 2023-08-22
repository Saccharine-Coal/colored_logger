from __future__ import annotations
import logging


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
    ):
        # https://www.w3.org/TR/xml-entity-names/025.html
        self.STR_TO_COLOR = {
            "": self.RESET,  # reset
            "BLACK": self.BLACK,  # foreground black
            "RED": self.RED,  # foreground red
            "GREEN": self.GREEN,  # foreground green
            "YELLOW": self.YELLOW,  # foreground yellow
            "BLUE": self.BLUE,  # foreground blue
            "MAGENTA": self.MAGENTA,  # foreground magenta
            "CYAN": self.CYAN,  # foreground cyan
            "WHITE": self.WHITE,  # foreground white
            "BLACK-BG": "\x1b[40m",  # bg black
            "RED-BG": "\x1b[41m",  # bg red
            "GREEN-BG": "\x1b[42m",  # foreground green
            "YELLOW-BG": "\x1b[43m",  # foreground yellow
            "BLUE-BG": "\x1b[44m",  # foreground blue
            "MAGENTA-BG": "\x1b[45m",  # foreground magenta
            "CYAN-BG": "\x1b[46m",  # foreground cyan
            "WHITE-BG": "\x1b[47m",  # foreground whit
        }
        self.INT_TO_STR: dict[int, str] = {
            0: "",
            logging.DEBUG: "MAGENTA",
            logging.INFO: "GREEN",
            logging.WARNING: "YELLOW",
            logging.ERROR: "RED",
            logging.CRITICAL: "RED",
        }
        self.ENDCAPS = {
            "left-triangle-filled": "\u25c0",
            "left-triangle": "\u25c1",
            "right-triangle": "\u25b7",
            "right-triangle-filled": "\u25b6",
            "square": "\u25a0",
            "diamond": "\u25c6",
            "full-block": "\u2588",
        }
        self.CONNECTORS = {
            "single": {},
            "double": {
                "down-and-right": "\u2554",
                "down-and-left": "\u2557",
                "vertical": "\u2551",
                "vertical-and-left": "\u2563",
                "vertical-and-right": "\u2560",
                "up-and-right": "\u255a",
                "up-and-left": "\u255d",
                "cross": "\u256c",
                "t-junction-up": "\u2569",
                "t-junction-down": "\u2566",
                "horizontal": "\u2550",
            },
        }
        self.name = name
        self.endcap = endcap
        self.connector = "double"
        self.connector_color = self.STR_TO_COLOR[connector_color.upper()]
        self.msg_length = 2
        self.msg_hspace = 1
        self.msg_tab = self.msg_length + 1 + self.msg_hspace
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
                print(
                    self.STR_TO_COLOR["CYAN-BG"] + self.BLACK + f" {name} " + self.RESET
                )
            print()
        # print(
        #     self.connector_color
        #     + self.CONNECTORS[self.connector]["vertical"]
        #     + self.RESET
        # )

    def _get_endcap(self, right=True) -> str:
        fmt = ""
        if self.endcap == "triangle-filled" or self.endcap == "triangle":
            if right:
                fmt = self.ENDCAPS["right-" + self.endcap]
            else:
                fmt = self.ENDCAPS["left-" + self.endcap]
                fmt = self.ENDCAPS["square"]
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
        header_fmt = f"\t\t{self.RESET}{self.CYAN}%(module)s.%(funcName)s():%(lineno)d{self.RESET}\n"

        # header_fmt_long = f"%(levelname)s:{self.RESET}\t\t{self.CYAN}%(module)s.%(funcName)s():%(lineno)d{self.RESET}\n"
        connector_fmt = self._get_arrow(
            length=self.msg_length, endcap_color=self._get_color(levelno)
        )
        message_fmt = "%(message)s" + self.RESET
        # FORMAT = f"%(levelname)s:{self.RESET}\t\t{self.CYAN}%(module)s.%(funcName)s():%(lineno)d{self.RESET}\n{self._get_arrow()}%(message)s"
        # LONGFORMAT = f"%(levelname)s:{self.RESET}\t{self.CYAN}%(module)s.%(funcName)s():%(lineno)d{self.RESET}\n ↪ %(message)s"
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


def get_logger(
    name: str = __name__, level: int = logging.WARN, **kwargs
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter(name, **kwargs))

    logger.addHandler(ch)
    # logger.info("func")
    return logger


if __name__ == "__main__":
    LOGGER = get_logger(
        level=logging.DEBUG,
        print_colors=False,
        print_arrows=False,
        connector_color="white",
    )
    LOGGER.debug("hi")
    LOGGER.info("hi")
    LOGGER.warning("hi")
    LOGGER.error("hi")
    LOGGER.critical("hi")
