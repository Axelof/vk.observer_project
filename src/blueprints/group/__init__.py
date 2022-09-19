from src.blueprints.group import control_menu, control_triggers, control_middlewares

group_bps = (control_menu.bp, control_triggers.bp, control_middlewares.bp)

__all__ = ("group_bps",)
