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
            *[_[0] for _ in re.compile(self.config.regexps.invite_links_pattern).findall(message.text)]
        ]
        return {"invite_links": invite_links}


class HasInviteLinksRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_, ignore_switch: bool = False):
        self.config: ConfigModel = config
        self.ignore_switch = ignore_switch

    async def check(self, message: Message) -> bool:
        invite_links = [
            *[_[0] for _ in re.compile(self.config.regexps.invite_links_pattern).findall(message.text)]
        ]

        if not self.ignore_switch:
            if not self.config.triggers.invite_links:
                return False

        return len(invite_links) != 0
