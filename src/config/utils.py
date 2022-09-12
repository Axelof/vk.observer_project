import os
import re
import sys
import time
from typing import Union

import yaml

from src.config import ConfigModel
from yaml import CLoader as YamlLoader
from loguru import logger


def get_config_from_file(filename: Union[str, bytes, os.PathLike]) -> ConfigModel:
    with open(filename, "r", encoding="utf-8") as f:
        config = get_config(f.read())
        f.close()
    return config


def get_config(string: Union[str, bytes]) -> ConfigModel:
    logger.remove()
    yaml_config: str = remove_comments_from_string(string)  # type: ignore
    dict_config: dict = yaml.load(yaml_config, YamlLoader)
    config: ConfigModel = ConfigModel(**dict_config)

    log_format = (
        "<magenta>AF</magenta> | "
        "<level>{level: <8}</level> | "
        "<italic><green>{time:YYYY-MM-DD HH:mm:ss}</green></italic> | "
        "{name}:{function}:{line} > <level>{message}</level>"
    )

    if not config.logging.log_console:
        logger.add(
            sys.stderr, format=log_format, level="INFO", enqueue=True, colorize=True
        )
    else:
        logger.add(sys.stderr, format=log_format, enqueue=True, colorize=True)

    if config.logging.log:
        enable_file_logging(
            time.strftime(config.logging.log_path),
            level=10 if config.logging.log_debug else 20,
            format=log_format,
            rotation="5 MB",
            compression="zip",
            retention="1 days",
        )

    if config.logging.log_errors:
        enable_file_logging(
            time.strftime(config.logging.log_errors_path),
            level=30,
            format=log_format,
            rotation="5 MB",
            compression="zip",
            retention="15 days",
        )

    return config


FINDALL_VALUES_PATTERN = re.compile(r"\${(\w+)}")
REMOVE_COMMENTS_FROM_STRING_PATTERN = re.compile(r"(?m)^ *#.*\n?")


def remove_comments_from_string(string: str):
    return REMOVE_COMMENTS_FROM_STRING_PATTERN.sub("", string)


def enable_file_logging(file: str, level: Union[str, int], **kwargs) -> int:
    return logger.add(file, level=level, **kwargs)


__all__ = (
    "get_config_from_file",
    "get_config",
)
