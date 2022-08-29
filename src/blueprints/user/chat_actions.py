from vkbottle.user import Message, rules

from src.blueprints.UserBlueprint import UserBlueprint


bp = UserBlueprint("user.chat_actions")
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True)]


@bp.on.message(rules.ChatActionRule(["chat_invite_user"]), blocking=False)
async def chat_invite_handler(message: Message):
    print(message.action)
