import re

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from src.config import ConfigModel as ConfigModel
from src.config import config as config_


class InviteLinksRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> dict:
        invite_links = [
            *re.compile(self.config.regexps.invite_links_pattern).findall(message.text)
        ]
        return {"invite_links": invite_links}


class HasInviteLinksRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> bool:
        links = [
            *re.compile(self.config.regexps.invite_links_pattern).findall(message.text)
        ]
        return len(links) != 0
