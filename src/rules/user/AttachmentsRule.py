import re

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from src.config import ConfigModel as ConfigModel
from src.config import config as config_


class AttachmentsRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> dict:
        triggered_attachments = []
        for attachment in message.get_attachment_strings():
            for k, v in self.config.triggers.attachments.dict().items():
                if v is True:
                    if attachment.startswith(k):
                        triggered_attachments.append(attachment)

        return {"attachments": triggered_attachments}


class HasAttachmentsRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_, ignore_switch: bool = False):
        self.config: ConfigModel = config

    async def check(self, message: Message) -> bool:
        triggered_attachments = []
        for attachment in message.get_attachment_strings():
            for k, v in self.config.triggers.attachments.dict().items():
                if v is True:
                    if attachment.startswith(k):
                        triggered_attachments.append(attachment)

        return len(triggered_attachments) != 0
