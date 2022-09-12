from src.blueprints import user_bps, group_bps
from src.middlewares import user_mws, group_mws
from src.user import User
from src.bot import Bot
from src.config import config
from src.utils import loop, loop_wrapper

# from src.database.db import database


user: User = (
    User(
        token=config.general.user.token,
        loop=loop,
        loop_wrapper=loop_wrapper,
    ).add_middleware(middleware=user_mws)
    #  .set_database(database)
)

bot: Bot = (
    Bot(
        token=config.general.group.token,
        loop=loop,
        loop_wrapper=loop_wrapper,
    ).add_middleware(middleware=group_mws)
    #  .set_database(database)
)

user.bot, bot.user = bot, user
user.add_blueprint(blueprint=user_bps)
bot.add_blueprint(blueprint=group_bps)

__all__ = ("user", "bot", "loop_wrapper")
