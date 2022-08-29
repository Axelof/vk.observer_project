from sys import platform
from vkbottle.tools.dev.loop_wrapper import LoopWrapper

if platform == "linux" or platform == "linux2":
    from uvloop import EventLoopPolicy
    loop = EventLoopPolicy()
elif platform.lower().startswith('win'):
    from asyncio import get_event_loop
    loop = get_event_loop()

loop_wrapper = LoopWrapper()


__all__ = (
    "loop",
    "loop_wrapper",
)
