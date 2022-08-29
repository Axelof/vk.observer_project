from vkbottle.user import Message, rules

from src.blueprints.BotBlueprint import BotBlueprint
from src.rules.group.InviteLinksRule import InviteLinksRule, HasInviteLinksRule

bp = BotBlueprint("group.invite_links")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), InviteLinksRule()]


@bp.on.chat_message(HasInviteLinksRule(), blocking=False)
async def invite_links_trigger(_: Message, invite_links: list):
    pass
