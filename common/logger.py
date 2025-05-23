import logging
import os
import re

def setup_logger(name: str, level=logging.INFO):
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

        # Determine next log file number
        existing_logs = [f for f in os.listdir("logs") if re.match(rf"{re.escape(name)}(\d*).log$", f)]
        numbers = [int(re.search(r"(\d+)", f).group(1)) for f in existing_logs if re.search(r"(\d+)", f)]
        next_num = max(numbers, default=0) + 1
        filename = f"logs/{name}{next_num}.log"

        # File handler
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger