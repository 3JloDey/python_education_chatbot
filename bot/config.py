from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Database:
    username: str
    password: str
    name: str
    host: str
    port: int


@dataclass
class Redis:
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str | None


@dataclass
class Hastebin:
    api_key: str


@dataclass
class Config:
    bot: TgBot
    storage: Redis
    database: Database
    hastebin: Hastebin


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=TgBot(token=env.str("BOT_TOKEN")),
        storage=Redis(
            redis_host=env.str("REDIS_HOST"),
            redis_port=env.int("REDIS_PORT"),
            redis_db=env.int("REDIS_DB"),
            redis_password=env.str("REDIS_PASSWORD"),
            ),
        hastebin=Hastebin(api_key=env.str("HASTEBIN_TOKEN")),
        database=Database(
            username=env.str("DB_USERNAME"),
            password=env.str("DB_PASSWORD"),
            name=env.str("DB_NAME"),
            host=env.str("DB_HOST"),
            port=env.str("DB_PORT"),
        ),
    )
