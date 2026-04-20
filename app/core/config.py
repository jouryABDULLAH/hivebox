from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_VERSION: str = "0.0.1"
    SENSEBOX_IDS: str = ""

    model_config = SettingsConfigDict(env_file=".env")

    @property 
    def sensebox_ids(self) -> list[str]:
        if not self.SENSEBOX_IDS:
            return []
        return [
            x.strip() # to get rid of accidental spcaes
            for x in self.SENSEBOX_IDS.split(",")
            ]




settings = Settings()
