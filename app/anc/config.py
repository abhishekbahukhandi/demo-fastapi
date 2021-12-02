from pydantic import BaseSettings
import os
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = "~/Desktop/python_files/fastapi_project/.env"
settings = Settings()
