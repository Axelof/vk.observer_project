from vkbottle.user import Message, rules
from vkbottle import vkscript


from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.MentionsRule import MentionsRule, HasMentionsRule
from src.config import config

bp = UserBlueprint("user.mentions")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), MentionsRule()]


@bp.on.chat_message(HasMentionsRule(), blocking=False)
async def mentions_trigger(message: Message, mentions: list):
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

    mentions = (
        await bp.bot.api.execute(
            code=validate_mentions(
                mentions=mentions, _id=["user", "id"], _club=["group", "club"]
            )
        )
    )["response"]

    await bp.bot.api.messages.send(
        user_id=config.bot.info.user_id,
        random_id=0,
        reply_to=reply_to,
        message="@club" if str(message.from_id).startswith("-") else "@id"
        + str(message.from_id)
        + f" упоминал: \n"
        + "\n".join([f"{_id+1}. @{mention}" for _id, mention in enumerate(mentions)]),
    )


@vkscript
def validate_mentions(api, mentions: list, _id: str, _club: str):
    validated_mentions = []
    for mention in mentions:
        response = api.utils.resolve_screen_name(screen_name=mention)
        if response.type == "_id[0]":
            validated_mentions.append("_id[1]" + response.object_id)
        if response.type == "_club[0]":
            validated_mentions.append("_club[1]" + response.object_id)

    return validated_mentions
