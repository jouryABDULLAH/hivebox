from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_VERSION: str = "0.0.0"
    SENSEBOX_IDS: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
