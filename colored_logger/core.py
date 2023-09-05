from __future__ import annotations
import logging

import colored_logger.colors as colors
import colored_logger.symbols as symbols


class CustomFormatter(logging.Formatter):
    def __init__(
        self,
        name: str = __name__,
        startcap="square-filled",
        endcap: str = "triangle-filled",
        connector: str = "double",
        connector_color: str = "",
        level: str = "WARN",
        msg_length: int = 6,
        msg_hspace: int = 1,
        num_tabs=10,
        shortend_names: bool = True,
        datefmt: str = "%Y-%m-%d %H:%H:%S",
        **formatter_kwargs,
    ):
        # NOTE: init arguments
        self.level = level.upper()  # convert lowercase to uppercase
        self.msg_length = msg_length  # how much spacing to put for printed msg
        self.msg_hspace = (
            msg_hspace
        )  # how much space between the start cap and log level
        self.num_tabs = (
            num_tabs
        )  # spacing between log level and other things on the level line
        self.name = name
        self.startcap = startcap
        self.endcap = endcap
        self.connector = connector
        self.connector_color = colors.COLORS[connector_color.upper()]
        self.shortend_names = shortend_names
        # NOTE: constants
        self.INT_TO_STR: dict[int, str] = {
            0: "",
            logging.DEBUG: "MAGENTA",
            logging.INFO: "GREEN",
            logging.WARNING: "YELLOW",
            logging.ERROR: "RED",
            logging.CRITICAL: "RED",
        }
        # NOTE: assign variables from given arguments
        self.msg_tab = self.msg_length + 1 + self.msg_hspace
        super().__init__(datefmt=datefmt, **formatter_kwargs)
        if self.shortend_names:
            self._shorten_names()
        self._print_init()

    def _print_init(self) -> None:
        """Print init with formatter name"""
        print(colors.BLACK + colors.COLORS["CYAN-BG"] + f" {self.name} " + colors.RESET)
        if self.connector_color:
            print(
                self.connector_color
                + symbols.CONNECTORS[self.connector]["vertical"]
                + colors.RESET
            )
        else:
            print()

    def _shorten_names(self) -> None:
        """Shorten default log names to 4 letter names.
        This is purely to align connectors and symbols."""
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
        for key, val in STR_TO_LOGLEVEL.items():
            logging.addLevelName(val, _SHORT_NAMES[key])

    def _get_endcap(self, right=True) -> str:
        fmt = ""
        if self.endcap == "triangle-filled" or self.endcap == "triangle":
            if right:
                fmt = symbols.ENDCAPS["right-" + self.endcap]
            else:
                fmt = symbols.ENDCAPS["left-" + self.endcap]
                fmt = symbols.ENDCAPS[self.startcap]
        elif self.endcap in symbols.ENDCAPS.keys():
            fmt = symbols.ENDCAPS[self.endcap]
        else:
            raise ValueError
        return fmt + " " * self.msg_hspace

    def _get_arrow(self, length=1, right=True, endcap_color="") -> str:
        connectors = symbols.CONNECTORS[self.connector]
        fmt = self.connector_color
        if self.connector_color == colors.RESET:
            connector = " "
        else:
            fmt += connectors["vertical-and-right"]
            connector = connectors["horizontal"]
        fmt += connector * length
        fmt += endcap_color + self._get_endcap(right=right)
        fmt += colors.RESET
        return fmt

    def _get_color(self, input, bg=False) -> str:
        def as_color_code(input_str: str, bg: bool) -> str:
            color_code = ""
            for color in input_str.split(","):
                if bg:
                    color += "-bg"
                color_code += colors.COLORS[color.upper()]
            return color_code

        if isinstance(input, int):
            return as_color_code(self.INT_TO_STR[input], bg)
        else:
            return as_color_code(input, bg)

    def _get_format(self, levelno: int) -> str:
        """Get format string for logger with color codes and symbols inserted."""
        start_cap = self._get_arrow(
            length=0, right=False, endcap_color=self._get_color(levelno)
        ) + self._get_color(levelno, bg=levelno == logging.CRITICAL)
        level_fmt = f"{start_cap}%(levelname)s{colors.RESET}:"
        white_space = "\t" * self.num_tabs
        module_fmt = f"{colors.CYAN}%(module)s.%(funcName)s():%(lineno)d{colors.RESET} "
        time_fmt = f"{colors.WHITE}%(asctime)s{colors.RESET}\n"
        connector_fmt = self._get_arrow(
            length=self.msg_length, endcap_color=self._get_color(levelno)
        )
        message_fmt = f"%(message)s{colors.RESET}"
        return (
            level_fmt
            + white_space
            + module_fmt
            + time_fmt
            + connector_fmt
            + message_fmt
        )

    def format(self, record):
        log_fmt = self._get_format(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        if "\n" in record.msg:  # insert decorations to message
            msg = ""
            for i, line in enumerate(record.msg.splitlines()):
                if i != 0:
                    msg += (
                        "\n"
                        + self.connector_color
                        + symbols.CONNECTORS[self.connector]["vertical"]
                        + colors.RESET
                        + " " * self.msg_tab
                    )
                msg += line
            record.msg = msg
        fmt = formatter.format(record)
        if "<module>()" in fmt:  # remove <module>
            fmt = fmt.replace(".<module>()", "")
        return fmt


def get_logger(formatter: CustomFormatter, config: dict = {}) -> logging.Logger:
    if not isinstance(formatter, logging.Formatter):
        raise TypeError(
            f"Formatter must be of type logging.Formatter not {type(formatter)}."
        )
    name, level = formatter.name, formatter.level
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug("Logging Configuration Complete!")
    return logger
