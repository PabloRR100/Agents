import os
import logging
import warnings
from typing import Optional
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning


def str_to_bool(value: str) -> bool:
    return value.lower() in ('true', '1', 't', 'y', 'yes')


load_dotenv()
VERBOSE = str_to_bool(os.getenv("VERBOSE_TRANSCRIPT_PARSING", "True"))


def setup_logging(
    log_level=os.getenv("LOG_LEVEL", logging.INFO),
    log_file: Optional[str] = None,
    filter_warnings: bool = True,
):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Create file handler
    file_handler = None
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        if file_handler is not None:
            logger.addHandler(file_handler)

    if filter_warnings:
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="setuptools")
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="transformers")
        warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
        warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub.file_download'")
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="turicreate._deps")
        warnings.filterwarnings("ignore", category=InsecureRequestWarning)
