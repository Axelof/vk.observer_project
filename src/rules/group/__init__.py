from src.rules.group.MentionsRule import MentionsRule, HasMentionsRule
from src.rules.group.InviteLinksRule import InviteLinksRule, HasInviteLinksRule
from src.rules.group.FromMeRule import FromMeRule
from src.rules.group.IsAdminRule import IsAdminRule

group_rules = (MentionsRule, HasMentionsRule, InviteLinksRule, HasInviteLinksRule, FromMeRule, IsAdminRule)

__all__ = (
    "group_rules",
    "MentionsRule", "HasMentionsRule",
    "InviteLinksRule", "HasInviteLinksRule",
    "FromMeRule", "IsAdminRule"
)