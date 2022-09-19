from vkbottle.bot import Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Callback, GroupEventType

from src.blueprints.BotBlueprint import BotBlueprint
from src.config import config

bp = BotBlueprint("group.control_triggers")


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
    keyboard.add(Callback("инвайт ссылки", {"event": "switch_trigger", "trigger": "invite_links"}),
                 color=ButtonColors.positive if config.triggers.invite_links else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("сокращённые ссылки", {"event": "switch_trigger", "trigger": "short_links"}),
                 color=ButtonColors.positive if config.triggers.short_links else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("приглашения", {"event": "switch_trigger", "trigger": "invites"}),
                 color=ButtonColors.positive if config.triggers.invites else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("упоминания", {"cmd": "triggers.mentions_menu"}),
                 color=ButtonColors.positive if config.triggers.mentions.user or config.triggers.mentions.group else ButtonColors.negative)
    return keyboard.get_json()


def get_mentions_menu_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Callback("назад", {"cmd": "triggers_menu"}),
                 color=ButtonColors.primary)
    keyboard.row()
    keyboard.add(Callback("пользователи", {"event": "switch_mentions_key", "key": "user"}),
                 color=ButtonColors.positive if config.triggers.mentions.user else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("группы", {"event": "switch_mentions_key", "key": "group"}),
                 color=ButtonColors.positive if config.triggers.mentions.group else ButtonColors.negative)
    return keyboard.get_json()


def get_text():
    return f"""
     список триггеров:
       1. инвайт ссылки: {"вкл." if config.triggers.invite_links else "выкл."}
       2. сокращённые ссылки: {"вкл." if config.triggers.short_links else "выкл."}
       3. приглашения {"вкл." if config.triggers.invites else "выкл."}
       4. упоминания: 
       — пользователи: {"вкл." if config.triggers.mentions.user else "выкл."}
       — группы: {"вкл." if config.triggers.mentions.group else "выкл."}
    """


def get_mentions_text():
    return f"""
     упоминания:
       — пользователи: {"вкл." if config.triggers.mentions.user else "выкл."}
       — группы: {"вкл." if config.triggers.mentions.group else "выкл."}
    """


@bp.on.private_message(text=[".триггеры", ".triggers"], blocking=False)
async def control_menu_switches(message: Message):
    await message.reply(get_text(), keyboard=get_control_menu_keyboard())


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"event": "switch_trigger"}) | rules.PayloadContainsRule({"cmd": "triggers_menu"}),
    blocking=False,
)
async def control_menu_event(event: MessageEvent):
    if event.payload.get("cmd") is None:
        dict_config = config.triggers.dict()
        dict_config[event.payload["trigger"]] = not dict_config[event.payload["trigger"]]
        config.triggers = config.triggers.parse_obj(dict_config)

    await event.edit_message(get_text(), keyboard=get_control_menu_keyboard(), keep_forward_messages=True)


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"event": "switch_mentions_key"}) | rules.PayloadContainsRule({"cmd": "triggers.mentions_menu"}),
    blocking=False,
)
async def mentions_menu_event(event: MessageEvent):
    if event.payload.get("cmd") is None:
        dict_config = config.triggers.mentions.dict()
        dict_config[event.payload["key"]] = not dict_config[event.payload["key"]]
        config.triggers.mentions = config.triggers.mentions.parse_obj(dict_config)

    await event.edit_message(get_mentions_text(), keyboard=get_mentions_menu_keyboard(), keep_forward_messages=True)
