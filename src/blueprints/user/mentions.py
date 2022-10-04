from vkbottle.user import Message, rules
from vkbottle import vkscript

from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.MentionsRule import MentionsRule, HasMentionsRule
from src.config import config


bp = UserBlueprint("user.mentions")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), MentionsRule()]


@bp.on.chat_message(HasMentionsRule(ignore_switch=True), blocking=False)  # эта функция будет выполняться вне зависимости от положения переключателя в конфиге.
async def mentions_trigger(message: Message, mentions: list):  # можно использовать, к примеру для сбора аналитики.
    pass


@bp.on.chat_message(HasMentionsRule(), blocking=False)
async def mentions_trigger(message: Message, mentions: list):
    mentions = (
        await bp.bot.api.execute(
            code=validate_mentions(
                mentions=mentions if len(mentions) <= 20 else [mentions[_] for _ in range(20)]
            )
        )
    )["response"]

    if not config.triggers.mentions.group:
        mentions = [mention for mention in mentions if mention.startswith("id")]

    if not config.triggers.mentions.user:
        mentions = [mention for mention in mentions if mention.startswith("club")]

    if len(mentions) == 0:
        return

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
        reply_to=reply_to,
        message=f"из \"{user_execute_response['title']}\" [{message.peer_id}]\n\n" +
        ("@club" if str(message.from_id).startswith("-") else "@id")
        + str(message.from_id).replace("-", "")
        + f" упоминал: \n"
        + "\n".join([f"{_id+1}. @{mention}" for _id, mention in enumerate(mentions)]),
    )

    await bp.api.messages.delete(message_ids=user_execute_response["message_id"])


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


@vkscript
def validate_mentions(api, mentions: list):
    validated_mentions = []
    for mention in mentions:
        response = api.utils.resolve_screen_name(screen_name=mention)
        if response.type == "user":
            validated_mentions.append("id" + response.object_id)
        if response.type == "group":
            validated_mentions.append("club" + response.object_id)

    return validated_mentions
