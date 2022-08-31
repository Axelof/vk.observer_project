from src.rules.user.MentionsRule import MentionsRule, HasMentionsRule
from src.rules.user.InviteLinksRule import InviteLinksRule, HasInviteLinksRule
from src.rules.user.ShortLinksRule import ShortLinksRule, HasShortLinksRule
from src.rules.user.FromMeRule import FromMeRule
from src.rules.user.IsAdminRule import IsAdminRule


user_rules = (
    MentionsRule, HasMentionsRule,
    InviteLinksRule, HasInviteLinksRule,
    ShortLinksRule, HasShortLinksRule,
    FromMeRule, IsAdminRule
)

__all__ = (
    "user_rules",
    "MentionsRule", "HasMentionsRule",
    "InviteLinksRule", "HasInviteLinksRule",
    "FromMeRule", "IsAdminRule"
)