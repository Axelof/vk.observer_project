from src.middlewares.user.NoGroupMiddleware import NoGroupMiddleware

user_mws = (NoGroupMiddleware,)

__all__ = ("user_mws",)
