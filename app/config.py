from typing import Literal

from pydantic import BaseSettings , root_validator

class Settings(BaseSettings):
    DB_HOST :str
    DB_PORT  : int
    DB_USER  :str
    DB_PASS  :str
    DB_NAME  :str

    secret_key:str
    algorutm:str

    REDIS_HOST : str
    REDIS_PORT : int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    MODE: Literal['DEV','TEST','PROD']
    LOG_LEVEL : str

    @root_validator
    def get_database_url(cls , v):
        v['DATABASE_URL'] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v

    test_DB_HOST: str
    test_DB_PORT: int
    test_DB_USER: str
    test_DB_PASS: str
    test_DB_NAME: str

    @root_validator
    def get_test_database_url(cls, v):
        v['test_DATABASE_URL'] = f"postgresql+asyncpg://{v['test_DB_USER']}:{v['test_DB_PASS']}@{v['test_DB_HOST']}:{v['test_DB_PORT']}/{v['test_DB_NAME']}"
        return v

    class Config:
        env_file = '.env'


settings = Settings()

