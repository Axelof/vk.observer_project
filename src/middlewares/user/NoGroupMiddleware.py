from vkbottle.bot import Message
from vkbottle import BaseMiddleware

from src.config import ConfigModel as ConfigModel
from src.config import config as config_


class NoGroupMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        config: ConfigModel = config_

        if config.middlewares.no_group_messages:
            if self.event.from_id < 0:
                self.stop("from_id меньше 0")
