import re

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from src.config import ConfigModel as ConfigModel
from src.config import config as config_


class ShortLinksRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> dict:
        short_links = [
            *re.compile(self.config.regexps.shortened_links_patterns).findall(
                message.text
            )
        ]
        return {"short_links": short_links}


class HasShortLinksRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> bool:
        short_links = [
            *re.compile(self.config.regexps.shortened_links_patterns).findall(
                message.text
            )
        ]
        return len(short_links) != 0
