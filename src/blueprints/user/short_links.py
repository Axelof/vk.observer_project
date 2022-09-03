from vkbottle.user import Message, rules
from vkbottle import vkscript

from src.blueprints.UserBlueprint import UserBlueprint
from src.rules.user.ShortLinksRule import ShortLinksRule, HasShortLinksRule
from src.config import config


bp = UserBlueprint("user.short_links")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), ShortLinksRule()]


@bp.on.chat_message(HasShortLinksRule(), blocking=False)
async def mentions_trigger(message: Message, short_links: list):
    await bp.api.messages.send(
        peer_id=-config.bot.info.group_id,
        message=None,
        random_id=0,
        forward={
            "peer_id": message.peer_id,
            "conversation_message_ids": message.conversation_message_id,
        },
    )

    execute_response = (
        await bp.bot.api.execute(
            code=validate_short_links(
                short_links=[_[0] for _ in short_links], invalid_url="http://vk.com/"
            )
        )
    )["response"]

    if len(execute_response["valid"]) != 0:
        valid_links = (
            "Рабочие:\n"
            + "\n".join(
                f"{_id + 1}. {link['cc']}\n— {link['url']}\n"
                for _id, link in enumerate(execute_response["valid"])
            )
            + "\n"
        )
    else:
        valid_links = ""

    if len(execute_response["invalid"]) != 0:
        invalid_links = (
            "Нерабочие:\n"
            + "\n".join(
                f"{_id + 1}. {link}\n"
                for _id, link in enumerate(execute_response["invalid"])
            )
            + "\n"
        )
    else:
        invalid_links = ""

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
        reply_to=reply_to,
        random_id=0,
        dont_parse_links=True,
        message=f"Обнаружены сокращённые ссылки! \n\n {valid_links} {invalid_links}",
    )


@vkscript
def validate_short_links(api, short_links: list, invalid_url: str):
    valid = []
    invalid = []
    for short_link in short_links:
        response = api.utils.check_link(url=short_link)

        if response.link != invalid_url:
            valid.append({"cc": short_link, "url": response.link})
        else:
            invalid.append(short_link)
    return {"valid": valid, "invalid": invalid}
