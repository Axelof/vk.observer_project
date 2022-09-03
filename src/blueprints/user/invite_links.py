from vkbottle.user import Message, rules
from vkbottle import vkscript

from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.InviteLinksRule import InviteLinksRule, HasInviteLinksRule
from src.config import config

bp = UserBlueprint("user.invite_links")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), InviteLinksRule()]


@bp.on.chat_message(HasInviteLinksRule(), blocking=False)
async def invite_links_trigger(message: Message, invite_links: list):
    await bp.api.messages.send(
        peer_id=-config.bot.info.group_id,
        message=None,
        random_id=0,
        forward={
            "peer_id": message.peer_id,
            "conversation_message_ids": message.conversation_message_id,
        },
    )

    reply_to = (
        (
            await bp.bot.api.messages.get_history(
                user_id=config.bot.info.user_id, count=1
            )
        )
        .items[0]
        .id
    )

    await bp.bot.api.messages.send(
        user_id=config.bot.info.user_id,
        random_id=0,
        dont_parse_links=True,
        reply_to=reply_to,
        message="Обнаружены инвайт ссылки!\n"
        + "\n".join(
            f"{_id+1}. {link}"
            for _id, link in enumerate([_[0] for _ in invite_links])
        ),
    )
