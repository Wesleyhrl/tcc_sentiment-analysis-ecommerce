import logging
import os
from datetime import datetime

def setup_logger():

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_dir = "./1_coleta/logs"
    log_file = os.path.join(log_dir, f"scraping_{timestamp}.log")

    # Criar pasta logs se não existir
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("scraping")
    logger.setLevel(logging.DEBUG)

    # Formatter estruturado
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # console mostra só INFO+
    console_handler.setFormatter(formatter)

    # Evitar duplicação
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
