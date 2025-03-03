from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database Settings
    MONGO_URI: str
    DB_NAME: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_HOUR: int

    # Auth Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    class Config:
        env_file = ".env"

settings = Settings()