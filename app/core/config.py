from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_VERSION: str = "0.0.3"
    SENSEBOX_IDS_RAW: str = ""

    # Redis/Valkey
    REDIS_HOST: str = "valkey-redis-master"
    REDIS_PORT: int = 6379
    
    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "password123"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def sensebox_ids(self) -> list[str]:
        if not self.SENSEBOX_IDS_RAW:
            return []
        return [
            x.strip()  # to get rid of accidental spcaes
            for x in self.SENSEBOX_IDS_RAW.split(",")
            ]


settings = Settings()
