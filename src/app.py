from .blueprints import user_bps, group_bps
from .middlewares import user_mws, group_mws
from .user import User
from .bot import Bot
from .config import config

from utils import loop, loop_wrapper

user: User = (
    User(
        token=config.bot.user_token,
        loop=loop,
        loop_wrapper=loop_wrapper,
    )
    .add_middleware(middleware=user_mws)
)

bot: Bot = (
    Bot(
        token=config.bot.group_token,
        loop=loop,
        loop_wrapper=loop_wrapper,
    )
    .add_middleware(middleware=group_mws)
)

user.bot, bot.user = bot, user
user.add_blueprint(blueprint=user_bps)
bot.add_blueprint(blueprint=group_bps)

__all__ = (
    "user",
    "bot",
    "loop_wrapper"
)
