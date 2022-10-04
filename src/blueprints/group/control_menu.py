from vkbottle.bot import Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Callback, GroupEventType

from src.blueprints.BotBlueprint import BotBlueprint

bp = BotBlueprint("group.control_menu")


class ButtonColors:
    positive = KeyboardButtonColor.POSITIVE
    negative = KeyboardButtonColor.NEGATIVE
    primary = KeyboardButtonColor.PRIMARY
    secondary = KeyboardButtonColor.SECONDARY


def get_control_menu_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Callback("триггеры", {"cmd": "triggers_menu"}),
                 color=ButtonColors.primary)
    keyboard.row()
    keyboard.add(Callback("мидлвари", {"cmd": "middlewares_menu"}),
                 color=ButtonColors.primary)
    keyboard.row()
    keyboard.add(Callback("закрыть", {"cmd": "close"}),
                 color=ButtonColors.secondary)
    return keyboard.get_json()


def get_text():
    return f"""
     список разделов:
        1. триггеры
        2. мидлвари
    """


@bp.on.private_message(text=[".меню", ".menu"], blocking=False)
async def control_menu_switches(message: Message):
    await message.reply(get_text(), keyboard=get_control_menu_keyboard())


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"cmd": "control_menu"}),
    blocking=False,
)
async def control_menu_event(event: MessageEvent):
    await event.edit_message(get_text(), keyboard=get_control_menu_keyboard(), keep_forward_messages=True)


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"cmd": "close"}),
    blocking=False,
)
async def control_menu_event(event: MessageEvent):
    await bp.api.messages.delete(peer_id=event.peer_id, cmids=event.conversation_message_id, delete_for_all=True)
