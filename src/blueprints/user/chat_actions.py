from vkbottle.user import Message, rules

from src.blueprints.UserBlueprint import UserBlueprint
from src.config import config

bp = UserBlueprint("user.chat_actions")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True)]


@bp.on.message(rules.ChatActionRule(["chat_kick_user"]), blocking=False)
async def chat_kick_handler(message: Message):
    if not config.triggers.invites:
        return

    title = (await bp.api.messages.get_conversations_by_id(peer_ids=message.peer_id)).items[0].chat_settings.title

    await bp.bot.api.messages.send(
        user_id=config.general.user.id,
        random_id=0,
        message=f"из \"{title}\" [{message.peer_id}]\n\n" +
                ("@club" if str(message.from_id).startswith("-") else "@id") + str(message.from_id).replace("-", "") +
                " исключил " +
                ("@club" if str(message.action.member_id).startswith("-") else "@id") + str(message.action.member_id).replace("-", "")
    )


@bp.on.message(rules.ChatActionRule(["chat_invite_user"]), blocking=False)
async def chat_invite_handler(message: Message):
    if not config.triggers.invites:
        return

    title = (await bp.api.messages.get_conversations_by_id(peer_ids=message.peer_id)).items[0].chat_settings.title

    await bp.bot.api.messages.send(
        user_id=config.general.user.id,
        random_id=0,
        message=f"из \"{title}\" [{message.peer_id}]\n\n" +
                (f"@id{message.from_id} пригласил " +
                 ("@club" if str(message.action.member_id).startswith("-") else "@id") + str(message.action.member_id).replace("-", ""))
        if not message.from_id == message.action.member_id else
        ("@club" if str(message.action.member_id).startswith("-") else "@id") + str(message.action.member_id).replace("-", "") +
        " вернулся в чат"
    )
