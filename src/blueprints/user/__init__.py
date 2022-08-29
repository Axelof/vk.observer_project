from src.blueprints.user import mentions, invite_links, chat_actions

user_bps = (mentions.bp, invite_links.bp, chat_actions.bp)

__all__ = (
    "user_bps",
)
