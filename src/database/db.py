import asyncio
import urllib.parse
from vkbottle.modules import logger

from src.config import config
from src.database.engine import DataBase

if not config.database.url:
    config.database.url = (
        f"mongodb://{config.database.user}:"
        f"{urllib.parse.quote_plus(urllib.parse.quote_plus(config.database.password))}@"
        f"{config.database.host}:{config.database.port}/"
        f"{config.database.database}"
    )

try:
    database = DataBase(
        config.database.url, config.database.database, config.database.collection
    )
finally:
    logger.info("Database connected")

__all__ = (database,)
