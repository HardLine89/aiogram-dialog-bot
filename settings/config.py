from aiogram import Bot
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    use_proxy: bool
    proxy_url: str | None
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    @property
    def db_url(self) -> str:
        """Генерация URL для подключения к базе данных."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}?async_fallback=True"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AppConfig:
    settings = Settings()
    bot = Bot(token=settings.bot_token)
