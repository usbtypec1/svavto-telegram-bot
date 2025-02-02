import json
import logging.config
import pathlib
from typing import Final, Any

from config import SRC_DIR

__all__ = (
    'create_logger',
    'setup_logging',
    'LOGGING_CONFIG_FILE_PATH',
    'load_logging_config_from_file',
)

LOGGING_CONFIG_FILE_PATH: Final[pathlib.Path] = (
        SRC_DIR.parent / 'logging_config.json'
)


def create_logger(name: str) -> logging.Logger:
    return logging.getLogger('app')


def load_logging_config_from_file(
        file_path: pathlib.Path = LOGGING_CONFIG_FILE_PATH,
) -> dict[str, Any]:
    config_json = file_path.read_text(encoding='utf-8')
    return json.loads(config_json)


def setup_logging(
        file_path: pathlib.Path = LOGGING_CONFIG_FILE_PATH,
) -> None:
    config = load_logging_config_from_file(file_path)
    logging.config.dictConfig(config)
