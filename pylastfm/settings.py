from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore'
    )
    API_KEY: str
    USER_AGENT: str
