#!/usr/bin/env python3

import colored_logger.colors
import colored_logger.core
import colored_logger.symbols

formatter = colored_logger.core.CustomFormatter("Example", level="DEBUG")
logger = colored_logger.core.get_logger(formatter)

for key, value in colored_logger.colors.FOREGROUND_COLORS.items():
    logger.debug(f"FOREGROUND: key={key}, {value}colored{colored_logger.colors.RESET}")
for key, value in colored_logger.colors.BACKGROUND_COLORS.items():
    logger.info(f"BACKGROUND: key={key}, {value}colored{colored_logger.colors.RESET}")

logger.warning("Warning")
logger.error("Error")
logger.critical("Critical")
