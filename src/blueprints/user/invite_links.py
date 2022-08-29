from vkbottle.user import Message, rules

from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.InviteLinksRule import InviteLinksRule, HasInviteLinksRule
from src.config import config

bp = UserBlueprint("user.invite_links")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), InviteLinksRule()]


@bp.on.chat_message(HasInviteLinksRule(), blocking=False)
async def invite_links_trigger(_: Message, invite_links: list):
    await bp.bot.api.messages.send(user_id=config.bot.info.user_id, message=invite_links, random_id=0)
