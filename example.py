#!/usr/bin/env python3

import colored_logger.colors
import colored_logger.core
import colored_logger.symbols

formatter = colored_logger.core.CustomFormatter(
    "Example", level="DEBUG", connector_color="WHITE"
)
log = colored_logger.core.get_logger(formatter)

for key, value in colored_logger.colors.FOREGROUND_COLORS.items():
    if key == "BLACK":
        value += colored_logger.colors.WHITE_BG
    log.debug(f"FOREGROUND: key={key}, {value}<|##|>{colored_logger.colors.RESET}")
for key, value in colored_logger.colors.BACKGROUND_COLORS.items():
    log.info(f"BACKGROUND: key={key}, {value}<|##|>{colored_logger.colors.RESET}")

log.warning("Warning")
log.error("Error")
log.critical("Critical")
