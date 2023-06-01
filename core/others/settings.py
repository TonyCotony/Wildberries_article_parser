import os
import sys
from dataclasses import dataclass
from environs import Env

os.chdir(sys.path[0])


@dataclass()
class Bots:
    bot_token: str
    post_channel: str
    you_kassa_token: str


@dataclass()
class User:
    admin_id: int
    user_id: int
    owner_link: str
    user_annotations: str
    by_user: str
    bot_name: str


@dataclass()
class Properties:
    photo_catalog: str
    minutes_before_notification: float
    minutes_for_fill_time: float


@dataclass()
class Db:
    redis: str
    user: str
    password: str
    database: str
    host: str


@dataclass()
class Settings:
    bots: Bots
    db: Db
    user: User
    properties: Properties


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return(Settings(
        bots=Bots(
            bot_token=env.str("BOT_TOKEN"),
            post_channel=env.str("POSTING_CHANNEL"),
            you_kassa_token=env.str("YOUKASSA_TOKEN")
        ),
        user=User(
            admin_id=env.int("ADMIN_ID"),
            user_id=env.int("USER_ID"),
            owner_link=env.str("OWNER_LINK"),
            user_annotations=env.str("USER_ANNOTATION"),
            by_user=env.str("USER_BY"),
            bot_name=env.str("BOT_NAME")
        ),
        db=Db(
            redis=env.str("DB_REDIS_DNS"),
            user=env.str("DB_USER"),
            host=env.str("DB_HOST"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_DATABASE")
        ),
        properties=Properties(
            photo_catalog=env.str("PHOTO_CATALOG"),
            minutes_before_notification=env.str("MINUTES_BEFORE_SERV"),
            minutes_for_fill_time=env.str("MINUTES_FOR_FILL_TIME")
        )
    ))


settings = get_settings('input')
