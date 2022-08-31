from src.blueprints.user import mentions, invite_links, chat_actions, short_links

user_bps = (mentions.bp, invite_links.bp, chat_actions.bp, short_links.bp)

__all__ = (
    "user_bps",
)
