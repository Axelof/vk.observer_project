from vkbottle.user import Message, rules
from vkbottle import vkscript

from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.InviteLinksRule import InviteLinksRule, HasInviteLinksRule
from src.config import config


bp = UserBlueprint("user.invite_links")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), InviteLinksRule()]


@bp.on.chat_message(HasInviteLinksRule(ignore_switch=True), blocking=False)  # эта функция будет выполняться вне зависимости от положения переключателя в конфиге.
async def invite_links_trigger(message: Message, invite_links: list):  # можно использовать, к примеру для сбора аналитики.
    pass


@bp.on.chat_message(HasInviteLinksRule(), blocking=False)
async def invite_links_trigger(message: Message, invite_links: list):
    user_execute_response = (
        await bp.api.execute(
            code=get_conversation_name_and_send_message(
                group_id=config.general.group.id,
                peer_id=message.peer_id,
                cmid=message.conversation_message_id
            )
        )
    )["response"]

    reply_to = (
        (
            await bp.bot.api.messages.get_history(
                user_id=config.general.user.id, count=1
            )
        ).items[0].id
    )

    await bp.bot.api.messages.send(
        user_id=config.general.user.id,
        random_id=0,
        dont_parse_links=True,
        reply_to=reply_to,
        message=f"из \"{user_execute_response['title']}\" [{message.peer_id}]\n\n" +
        "Обнаружены инвайт ссылки!\n"
        + "\n".join(
            f"{_id+1}. {link}"
            for _id, link in enumerate(invite_links)
        ),
    )

    await bp.api.messages.delete(message_ids=user_execute_response["message_id"], delete_for_all=True)


@vkscript
def get_conversation_name_and_send_message(api, group_id: int, peer_id: int, cmid: int):
    message_id = api.messages.send(
        peer_id=-group_id,
        message=None,
        random_id=0,
        forward=f'{{"peer_id": {peer_id}, "conversation_message_ids": {cmid}}}',
    )
    conversation_name = api.messages.get_conversations_by_id(
        peer_ids=peer_id
    ).items
    return {"message_id": message_id, "title": conversation_name.pop().chat_settings.title}
