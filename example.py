#!/usr/bin/env python3
import logging

import colored_logger.colors
import colored_logger.core
import colored_logger.symbols
import colored_logger.colors as colors

colored_logger.set_formatter(
    colored_logger.CustomFormatter(
        name="Example", level="DEBUG", connector_color="WHITE"
    )
)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

for key, value in colored_logger.colors.FOREGROUND_COLORS.items():
    if key == "BLACK":
        value += colored_logger.colors.WHITE_BG
    log.debug(f"FOREGROUND: key={key}, {value}<|##|>{colored_logger.colors.RESET}")
for key, value in colored_logger.colors.BACKGROUND_COLORS.items():
    log.info(f"BACKGROUND: key={key}, {value}<|##|>{colored_logger.colors.RESET}")
for key, value in colored_logger.symbols.ENDCAPS.items():
    log.info(f"ENDCAPS: key={key}, {value}")
for key, dict in colored_logger.symbols.CONNECTORS.items():
    for subkey, value in dict.items():
        log.info(f"CONNECTORS: key={key}, subkey={subkey}, {value}")

log.warning("Warning")
log.error("Error")
log.critical("Critical")
