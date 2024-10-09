from typing import Any

from pydantic import HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ('Config', 'load_config_from_env_vars')


class Config(BaseSettings):
    telegram_bot_token: str
    api_base_url: HttpUrl
    admin_user_ids: set[int]

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    @field_validator('admin_user_ids', mode='before')
    @classmethod
    def validate_admin_user_ids(cls, value: Any) -> set[int]:
        return {int(user_id) for user_id in str(value).split(',')}


def load_config_from_env_vars() -> Config:
    return Config()
