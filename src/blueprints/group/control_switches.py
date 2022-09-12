from vkbottle.bot import Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Callback, GroupEventType

from src.blueprints.BotBlueprint import BotBlueprint
from src.config import config

bp = BotBlueprint("group.control_switches")


class ButtonColors:
    positive = KeyboardButtonColor.POSITIVE
    negative = KeyboardButtonColor.NEGATIVE


def get_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Callback("инвайт ссылки", {"cmd": "switch_trigger", "trigger": "invite_links"}),
                 color=ButtonColors.positive if config.triggers.invite_links else ButtonColors.negative)
    keyboard.add(Callback("упоминания", {"cmd": "switch_trigger", "trigger": "mentions"}),
                 color=ButtonColors.positive if config.triggers.mentions else ButtonColors.negative)
    keyboard.add(Callback("сокращённые ссылки", {"cmd": "switch_trigger", "trigger": "short_links"}),
                 color=ButtonColors.positive if config.triggers.short_links else ButtonColors.negative)
    return keyboard.get_json()


def get_text():
    return f"""
     список триггеров:
        1. инвайт ссылки: {"вкл." if config.triggers.invite_links else "выкл."}
        2. упоминания: {"вкл." if config.triggers.mentions else "выкл."}
        3. сокращённые ссылки: {"вкл." if config.triggers.short_links else "выкл."}
    """


@bp.on.private_message(text=".триггеры", blocking=False)
async def control_menu_switches(message: Message):
    await message.reply(get_text(), keyboard=get_keyboard())


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"cmd": "switch_trigger"}),
    blocking=False,
)
async def control_menu_event(event: MessageEvent):
    dict_config = config.triggers.dict()
    dict_config[event.payload["trigger"]] = not dict_config[event.payload["trigger"]]
    config.triggers = config.triggers.parse_obj(dict_config)

    await event.edit_message(get_text(), keyboard=get_keyboard(), keep_forward_messages=True)
