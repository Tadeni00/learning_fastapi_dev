from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    api_key: str = Field(alias="API_KEY")

    class Config:
        env_file = ".env"
        
settings = Settings()
