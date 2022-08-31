import asyncio
from typing import TYPE_CHECKING, NoReturn, Optional, Tuple, Union, List, Any

from vkbottle.api import API
from vkbottle.callback import BotCallback
from vkbottle.dispatch import BuiltinStateDispenser, Router
from vkbottle.exception_factory import ErrorHandler
from vkbottle.framework.abc import ABCFramework
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import logger
from vkbottle.polling import BotPolling
from vkbottle.tools import LoopWrapper

from .blueprints.ABCBlueprint import ABCBlueprint
from .config import config

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, Token
    from vkbottle.callback import ABCCallback
    from vkbottle.dispatch import ABCRouter, ABCStateDispenser
    from vkbottle.exception_factory import ABCErrorHandler
    from vkbottle.framework.labeler import ABCLabeler
    from vkbottle.polling import ABCPolling


class Bot(ABCFramework):
    def __init__(
        self,
        token: Optional["Token"] = None,
        api: Optional["ABCAPI"] = None,
        polling: Optional["ABCPolling"] = None,
        callback: Optional["ABCCallback"] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        loop_wrapper: Optional[LoopWrapper] = None,
        router: Optional["ABCRouter"] = None,
        labeler: Optional["ABCLabeler"] = None,
        state_dispenser: Optional["ABCStateDispenser"] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
        task_each_event: bool = True,
        db=None,
        user=None
    ):
        self.api: API = API(token) if token is not None else api  # type: ignore
        self.error_handler = error_handler or ErrorHandler()
        self.loop_wrapper = loop_wrapper or LoopWrapper()
        self.labeler = labeler or BotLabeler()
        self.state_dispenser = state_dispenser or BuiltinStateDispenser()
        self._polling = polling or BotPolling(self.api)
        self._callback = callback or BotCallback()
        self._router = router or Router()
        self._loop = loop
        self.task_each_event = task_each_event
        self.db = db
        self.user = user

    def set_database(self, db):
        self.db = db
        return self

    def add_blueprint(self, blueprint: Union[ABCBlueprint, List[ABCBlueprint]]):
        if isinstance(blueprint, (list, tuple)):
            for blueprint_ in blueprint:
                blueprint_.load(framework=self)
        else:
            blueprint.load(framework=self)

        return self

    def add_middleware(self, middleware: Any):
        if isinstance(middleware, (list, tuple)):
            for middleware_ in middleware:
                self.labeler.message_view.register_middleware(middleware=middleware_)
        else:
            self.labeler.message_view.register_middleware(middleware=middleware)

        return self

    @property
    def polling(self) -> "ABCPolling":
        return self._polling.construct(self.api, self.error_handler)

    @property
    def router(self) -> "ABCRouter":
        return self._router.construct(
            views=self.labeler.views(),
            state_dispenser=self.state_dispenser,
            error_handler=self.error_handler,
        )

    @router.setter
    def router(self, new_router: "ABCRouter"):
        self._router = new_router

    @property
    def on(self) -> "ABCLabeler":
        return self.labeler

    async def run_polling(self, custom_polling: Optional["ABCPolling"] = None):
        polling = custom_polling or self.polling
        config.bot.info.group_id = (await polling.api.groups.get_by_id())[0].id
        logger.info("Starting polling for @club{!r}", config.bot.info.group_id)

        async for event in polling.listen():
            logger.debug("New event was received: {}", event)
            for update in event["updates"]:
                if not self.task_each_event:
                    await self.router.route(update, polling.api)
                else:
                    self.loop.create_task(self.router.route(update, polling.api))

    def run_forever(self) -> NoReturn:  # type: ignore
        logger.info("Loop will be ran forever")
        self.loop_wrapper.add_task(self.run_polling())
        self.loop_wrapper.run_forever(self.loop)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    @loop.setter
    def loop(self, new_loop: asyncio.AbstractEventLoop):
        self._loop = new_loop
