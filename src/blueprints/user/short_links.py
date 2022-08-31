from vkbottle.user import Message, rules

from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.ShortLinksRule import ShortLinksRule, HasShortLinksRule
from src.config import config

bp = UserBlueprint("user.short_links")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), ShortLinksRule()]


@bp.on.chat_message(HasShortLinksRule(), blocking=False)
async def mentions_trigger(_: Message, short_links: list):
    print(short_links)
    await bp.bot.api.messages.send(user_id=config.bot.info.user_id, message=short_links, random_id=0)


