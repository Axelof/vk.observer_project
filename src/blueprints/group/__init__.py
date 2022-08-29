from src.blueprints.group import mentions, invite_links, chat_actions

group_bps = (mentions.bp, invite_links.bp, chat_actions.bp)

__all__ = ("group_bps",)