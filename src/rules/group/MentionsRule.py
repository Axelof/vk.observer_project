import re

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from src.config import ConfigModel as ConfigModel
from src.config import config as config_


class MentionsRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> dict:
        mentions = [
            *re.compile(self.config.regexps.links_pattern).findall(message.text),
            *re.compile(self.config.regexps.hyperlinks_pattern).findall(message.text)
        ]
        return {"mentions": mentions}


class HasMentionsRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> bool:
        mentions = [
            *re.compile(self.config.regexps.links_pattern).findall(message.text),
            *re.compile(self.config.regexps.hyperlinks_pattern).findall(message.text)
        ]
        return len(mentions) != 0
