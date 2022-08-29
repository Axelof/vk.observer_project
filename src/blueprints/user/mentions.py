from vkbottle.user import Message, rules

from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.MentionsRule import MentionsRule, HasMentionsRule
from src.config import config

bp = UserBlueprint("user.mentions")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), MentionsRule()]


@bp.on.chat_message(HasMentionsRule(), blocking=False)
async def mentions_trigger(_: Message, mentions: list):
    await bp.bot.api.messages.send(user_id=config.bot.info.user_id, message=mentions, random_id=0)


