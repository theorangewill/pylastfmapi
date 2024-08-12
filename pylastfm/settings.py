from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class is used to define and validate application settings using
    Pydantic's `BaseSettings` functionality. Settings are loaded from an
    environment file specified in the configuration.

    Attributes:
        API_KEY (str): The API key used for authentication.
        USER_AGENT (str): The user agent string to be used in HTTP requests.

    Config:
        - `env_file` is '.env': Path to the environment file from which
            to load the settings. In this case, it will need to be created a
            '.env' file in project root.
        - `extra` is 'ignored': How to handle extra fields. In this case, extra
            fields in the environment file will be ignored.
    """

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    API_KEY: str
    USER_AGENT: str
