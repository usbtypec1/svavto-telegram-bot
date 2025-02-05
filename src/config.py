import pathlib
import tomllib
from dataclasses import dataclass
from typing import Final

from zoneinfo import ZoneInfo

__all__ = ('Config', 'load_config_from_file', 'SRC_DIR', 'CONFIG_FILE_PATH')

SRC_DIR = pathlib.Path(__file__).parent
CONFIG_FILE_PATH: Final[pathlib.Path] = pathlib.Path(
    SRC_DIR.parent / 'config.toml',
)


@dataclass(frozen=True, slots=True)
class SentryConfig:
    dsn: str
    is_enabled: bool
    traces_sample_rate: float


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportTable:
    name: str
    url: str


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    api_base_url: str
    main_chat_id: int
    web_app_base_url: str
    timezone: ZoneInfo
    admin_user_ids_ttl_in_seconds: int
    report_tables: list[ReportTable]
    sentry: SentryConfig
    redis_url: str
    shifts_table_url: str


def load_config_from_file(
        config_file_path: pathlib.Path = CONFIG_FILE_PATH,
) -> Config:
    config_toml = config_file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_toml)

    report_tables = [
        ReportTable(
            name=report_table['name'],
            url=report_table['url'],
        )
        for report_table in config['report_tables']
    ]

    return Config(
        telegram_bot_token=config['telegram_bot']['token'],
        api_base_url=config['app']['api_base_url'],
        main_chat_id=config['app']['main_chat_id'],
        timezone=ZoneInfo(config['app']['timezone']),
        web_app_base_url=config['web_app']['base_url'].rstrip('/'),
        admin_user_ids_ttl_in_seconds=(
            config['app']['admin_user_ids_ttl_in_seconds']
        ),
        shifts_table_url=config['shifts_table']['url'],
        report_tables=report_tables,
        sentry=SentryConfig(
            dsn=config['sentry']['dsn'],
            is_enabled=config['sentry']['is_enabled'],
            traces_sample_rate=config['sentry']['traces_sample_rate'],
        ),
        redis_url=config['redis']['url'],
    )
