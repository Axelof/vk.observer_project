from vkbottle.user import Message
from vkbottle.dispatch.rules import ABCRule

from src.config import ConfigModel as ConfigModel
from src.config import config as config_


class IsAdminRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, event: Message) -> bool:
        return event.from_id in self.config.bot.admins
