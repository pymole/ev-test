from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    admin_api_key: str

    redis_url: RedisDsn

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str

    manipulator_host: str
    manipulator_port: int

    class Config:
        env_file = '.env'


global_settings = Settings()
