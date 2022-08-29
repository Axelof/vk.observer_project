from vkbottle.user import Message, rules

from src.blueprints.BotBlueprint import BotBlueprint
from src.rules.group.MentionsRule import MentionsRule, HasMentionsRule

bp = BotBlueprint("group.mentions")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), MentionsRule()]


@bp.on.chat_message(HasMentionsRule(), blocking=False)
async def mentions_trigger(_: Message, mentions: list):
    pass


