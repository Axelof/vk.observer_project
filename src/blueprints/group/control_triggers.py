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
                 color=ButtonColors.positive if True in [_ for _ in config.triggers.mentions.dict().values()] else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("вложения", {"cmd": "triggers.attachments_menu"}),
                 color=ButtonColors.positive if True in [_ for _ in config.triggers.attachments.dict().values()] else ButtonColors.negative)
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


def get_attachments_menu_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Callback("назад", {"cmd": "triggers_menu"}),
                 color=ButtonColors.primary)
    keyboard.row()
    keyboard.add(Callback("фото", {"event": "switch_attachments_key", "key": "photo"}),
                 color=ButtonColors.positive if config.triggers.attachments.photo else ButtonColors.negative)
    keyboard.add(Callback("аудио", {"event": "switch_attachments_key", "key": "audio"}),
                 color=ButtonColors.positive if config.triggers.attachments.audio else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("видео", {"event": "switch_attachments_key", "key": "video"}),
                 color=ButtonColors.positive if config.triggers.attachments.video else ButtonColors.negative)
    keyboard.add(Callback("документы", {"event": "switch_attachments_key", "key": "doc"}),
                 color=ButtonColors.positive if config.triggers.attachments.doc else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("товары", {"event": "switch_attachments_key", "key": "market"}),
                 color=ButtonColors.positive if config.triggers.attachments.market else ButtonColors.negative)
    keyboard.add(Callback("статьи", {"event": "switch_attachments_key", "key": "article"}),
                 color=ButtonColors.positive if config.triggers.attachments.article else ButtonColors.negative)
    keyboard.row()
    keyboard.add(Callback("истории", {"event": "switch_attachments_key", "key": "story"}),
                 color=ButtonColors.positive if config.triggers.attachments.story else ButtonColors.negative)
    keyboard.add(Callback("граффити", {"event": "switch_attachments_key", "key": "graffiti"}),
                 color=ButtonColors.positive if config.triggers.attachments.graffiti else ButtonColors.negative)
    return keyboard.get_json()


def get_text():
    return f"""
     список триггеров:
       1. инвайт ссылки: {"вкл." if config.triggers.invite_links else "выкл."}
       2. сокращённые ссылки: {"вкл." if config.triggers.short_links else "выкл."}
       3. приглашения {"вкл." if config.triggers.invites else "выкл."}
       4. упоминания {"вкл" if len([_ for _ in config.triggers.mentions.dict().values() if _ is True]) != 0 else "выкл"}
       5. вложения {"вкл" if len([_ for _ in config.triggers.attachments.dict().values() if _ is True]) != 0 else "выкл"}
    """


def get_mentions_text():
    return f"""
     упоминания:
       — пользователи: {"вкл." if config.triggers.mentions.user else "выкл."}
       — группы: {"вкл." if config.triggers.mentions.group else "выкл."}
    """


def get_attachments_text():
    return f"""
     вложения:
       — фото: {"вкл." if config.triggers.attachments.photo else "выкл."}
       — аудио: {"вкл." if config.triggers.attachments.audio else "выкл."}
       — видео: {"вкл." if config.triggers.attachments.video else "выкл."}
       — документы: {"вкл." if config.triggers.attachments.doc else "выкл."}
       — товары: {"вкл." if config.triggers.attachments.market else "выкл."}
       — статьи: {"вкл." if config.triggers.attachments.article else "выкл."}
       — истории: {"вкл." if config.triggers.attachments.story else "выкл."}
       — граффити: {"вкл." if config.triggers.attachments.graffiti else "выкл."}
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


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"event": "switch_attachments_key"}) | rules.PayloadContainsRule({"cmd": "triggers.attachments_menu"}),
    blocking=False,
)
async def mentions_menu_event(event: MessageEvent):
    if event.payload.get("cmd") is None:
        dict_config = config.triggers.attachments.dict()
        dict_config[event.payload["key"]] = not dict_config[event.payload["key"]]
        config.triggers.attachments = config.triggers.attachments.parse_obj(dict_config)

    await event.edit_message(get_attachments_text(), keyboard=get_attachments_menu_keyboard(), keep_forward_messages=True)
