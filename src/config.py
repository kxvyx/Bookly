from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env",
                                      extra ="ignore",
                                      env_file_encoding="utf-8")

#access any env variable by calling Config.<ENV_VARIABLE_NAME>
Config = Settings()