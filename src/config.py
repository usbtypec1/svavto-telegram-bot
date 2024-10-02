from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ('Config', 'load_config_from_env_vars')



class Config(BaseSettings):
    telegram_bot_token: str
    api_base_url: HttpUrl

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


def load_config_from_env_vars() -> Config:
    return Config()
