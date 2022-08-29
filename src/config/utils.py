import os
import re
import sys
import time
from typing import Union

import yaml

from src.config import ConfigModel
from yaml import CLoader as YamlLoader
from vkbottle.modules import logger as project_logger


def get_config_from_file(filename: Union[str, bytes, os.PathLike]) -> ConfigModel:
    with open(filename, "r", encoding="utf-8") as f:
        config = get_config(f.read())
        f.close()
    return config


def get_config(string: Union[str, bytes]) -> ConfigModel:
    yaml_config: str = remove_comments_from_string(string)  # type: ignore
    dict_config: dict = yaml.load(yaml_config, YamlLoader)
    dict_config["eal"] = dict(key="value")

    config: ConfigModel = ConfigModel(**dict_config)

    if not config.logging.log_console:
        project_logger.remove()
        project_logger.add(sys.stderr, level="INFO")

    if config.logging.log:
        enable_file_logging(time.strftime(config.logging.log_path), level=10 if not config.logging.log_disable_debug else 20, logger=project_logger)

    if config.logging.log_errors:
        enable_file_logging(time.strftime(config.logging.log_errors_path), level=30, logger=project_logger)

    return config


FINDALL_VALUES_PATTERN = re.compile(r"\${(\w+)}")
REMOVE_COMMENTS_FROM_STRING_PATTERN = re.compile(r"(?m)^ *#.*\n?")


def remove_comments_from_string(string: str):
    return REMOVE_COMMENTS_FROM_STRING_PATTERN.sub("", string)


def enable_file_logging(file: str, level: Union[str, int], logger, **kwargs) -> int:
    return logger.add(file, level=level, retention="10 seconds", **kwargs)


__all__ = (
    "get_config_from_file",
    "get_config",
)
