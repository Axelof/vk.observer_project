import urllib.parse
from src.config import config
from src.database.engine import DataBase

if not config.database.url:
    config.database.url = (
        f"mongodb://{config.database.user}:"
        f"{urllib.parse.quote_plus(urllib.parse.quote_plus(config.database.password))}@"
        f"{config.database.host}:{config.database.port}/"
        f"{config.database.database}"
    )

database = DataBase(
    config.database.url, config.database.database, config.database.collection
)

__all__ = (database,)
