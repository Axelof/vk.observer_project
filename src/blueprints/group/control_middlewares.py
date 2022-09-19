from vkbottle.bot import Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Callback, GroupEventType

from src.blueprints.BotBlueprint import BotBlueprint
from src.config import config

bp = BotBlueprint("group.control_middlewares")


class ButtonColors:
    positive = KeyboardButtonColor.POSITIVE
    negative = KeyboardButtonColor.NEGATIVE
    primary = KeyboardButtonColor.PRIMARY
    secondary = KeyboardButtonColor.SECONDARY


def get_control_menu_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Callback("в меню", {"cmd": "control_menu"}),
                 color=ButtonColors.primary)
    keyboard.row()
    keyboard.add(Callback("сообщения групп", {"event": "switch_middleware", "middleware": "no_group_messages"}),
                 color=ButtonColors.positive if config.middlewares.no_group_messages else ButtonColors.negative)
    return keyboard.get_json()


def get_text():
    return f"""
    список мидлварей:
      1. игнорирование групп: {"вкл." if config.middlewares.no_group_messages else "выкл."}
    """


@bp.on.private_message(text=[".мидлвари", ".middlewares"], blocking=False)
async def control_menu_switches(message: Message):
    await message.reply(get_text(), keyboard=get_control_menu_keyboard())


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"event": "switch_middleware"}) | rules.PayloadContainsRule({"cmd": "middlewares_menu"}),
    blocking=False,
)
async def control_menu_event(event: MessageEvent):
    if event.payload.get("cmd") is None:
        dict_config = config.middlewares.dict()
        dict_config[event.payload["middleware"]] = not dict_config[event.payload["middleware"]]
        config.middlewares = config.middlewares.parse_obj(dict_config)

    await event.edit_message(get_text(), keyboard=get_control_menu_keyboard(), keep_forward_messages=True)

