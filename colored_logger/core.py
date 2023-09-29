from __future__ import annotations
import logging
import os
import textwrap

from . import colors
from . import symbols


class CustomFormatter(logging.Formatter):
    ID = (
        "colored_logger"
    )  # NOTE: use this for global logger use. Either get_logger() or logging.getLogger("colored_logger")
    INT_TO_STR: dict[int, str] = {
        0: "",
        logging.DEBUG: "MAGENTA",
        logging.INFO: "GREEN",
        logging.WARNING: "YELLOW",
        logging.ERROR: "RED",
        logging.CRITICAL: "RED",
    }
    FLAG: str = "-.-"  # NOTE for right alignment

    def __init__(
        self,
        name: str = "main",
        startcap="square-filled",
        endcap: str = "triangle-filled",
        connector: str = "double",
        connector_color: str = "",
        level: str = "WARN",
        msg_length: int = 6,
        msg_hspace: int = 1,
        shortend_names: bool = True,
        datefmt: str = "%H:%H:%S",
        **formatter_kwargs,
    ):
        # NOTE: init arguments
        self.level = level.upper()  # convert lowercase to uppercase
        self.msg_length = msg_length  # how much spacing to put for printed msg
        self.msg_hspace = (
            msg_hspace
        )  # how much space between the start cap and log level
        self.name = name
        self.startcap = startcap
        self.endcap = endcap
        self.connector = connector
        self.connector_color = colors.COLORS[connector_color.upper()]
        self.shortend_names = shortend_names
        # NOTE: assign variables from given arguments
        self.msg_tab = self.msg_length + 1 + self.msg_hspace
        super().__init__(datefmt=datefmt, **formatter_kwargs)
        if self.shortend_names:
            self._shorten_names()
        self._print_init()
        self.term_size = (
            os.get_terminal_size()
        )  # NOTE: namedtuple os.terminal_size(columns=190, lines=46)
        self._count = 0  # a counter for right alignment TODO: need to make it work
        self._max_width = round(0.60 * self.term_size.columns)  # max term width ratio

    def _print_init(self) -> None:
        """Print init with formatter name"""
        print(colors.BLACK + colors.COLORS["CYAN-BG"] + f" {self.name} " + colors.RESET)
        if self.connector_color != colors.RESET:
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
                fmt = symbols.ENDCAPS[self.startcap]
        elif self.endcap in symbols.ENDCAPS.keys():
            fmt = symbols.ENDCAPS[self.endcap]
        else:
            raise ValueError
        return fmt + " " * self.msg_hspace

    def _get_arrow(self, length=1, right=True, endcap_color="", msg="", bg="") -> str:
        connectors = symbols.CONNECTORS[self.connector]
        if self.connector_color == colors.RESET:  # whitespace for connectors
            fmt = " " * length
        else:
            fmt = self._color_str(
                connectors["vertical-and-right"] + connectors["horizontal"] * length,
                self.connector_color,
            )
        fmt += self._color_str(self._get_endcap(right=right) + msg, endcap_color, bg=bg)
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

    def _color_str(self, string: str, fg: str, bg="") -> str:
        """Function to keep count of offset needed for color padding."""
        self._count += (
            len(fg) + len(colors.RESET) + len(bg)
        )  # size of color code and reset
        return fg + bg + string + colors.RESET

    def _get_format(self, levelno: int) -> str:
        """Get format string for logger with color codes and symbols inserted."""
        self._count = 0

        level_fmt = (
            self._get_arrow(
                length=0,
                right=False,
                endcap_color=self._get_color(levelno),
                msg="%(levelname)s",
                bg=self._get_color(levelno, bg=levelno == logging.CRITICAL),
            )
            + ":"
        )
        module_fmt = self._color_str(
            "%(module)s.%(funcName)s():%(lineno)s", colors.CYAN
        )
        time_fmt = self._color_str("%(asctime)s ", colors.WHITE)
        connector_fmt = self._get_arrow(
            length=self.msg_length, endcap_color=self._get_color(levelno)
        )
        message_fmt = "%(message)s"
        return (
            level_fmt
            + self.FLAG
            + time_fmt
            + module_fmt
            + "\n"
            + connector_fmt
            + self.FLAG
            + message_fmt
        )

    def format(self, record):
        log_fmt = self._get_format(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        record.msg = str(record.msg)  # convert types to string
        if len(record.msg) >= self._max_width and "\n" not in record.msg:
            record.msg = textwrap.fill(record.msg, self._max_width)
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
        head, body, tail = fmt.split(self.FLAG)
        fmt = head + " " * (self.term_size.columns - self._count) + body + tail
        return fmt


def set_formatter(formatter: CustomFormatter) -> None:
    if not isinstance(formatter, CustomFormatter):
        raise TypeError(
            f"Formatter must be of type CustomFormatter not {type(formatter)}."
        )

    logger = logging.getLogger()  # get root logger
    ch = logging.StreamHandler()
    ch.setFormatter(
        formatter
    )  # HACK: set formatter for root logger. All children of root will use this logger
    logger.addHandler(ch)
