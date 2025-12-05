from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_name: str 
    application_name: str = "The ticketing system"
    database_username: str
    database_password: str
    database_host: str
    database_port: str
    SECRET_KEY: str
    ALGORITHM: str


config = Settings()

