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
            *[_[0] for _ in re.compile(self.config.regexps.shortened_links_patterns).findall(message.text)]
        ]
        return {"short_links": short_links}


class HasShortLinksRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_, ignore_switch: bool = False):
        self.config: ConfigModel = config
        self.ignore_switch = ignore_switch

    async def check(self, message: Message) -> bool:
        short_links = [
            *[_[0] for _ in re.compile(self.config.regexps.shortened_links_patterns).findall(message.text)]
        ]

        if not self.ignore_switch:
            if not self.config.triggers.short_links:
                return False

        return len(short_links) != 0
