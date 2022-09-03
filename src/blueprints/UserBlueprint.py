from typing import TYPE_CHECKING, Optional, Union, Any

from pymongo.database import Database
from vkbottle.dispatch import Router
from vkbottle.framework.labeler import UserLabeler
from vkbottle.modules import logger

from .ABCBlueprint import ABCBlueprint
from src.user import User
from src.bot import Bot

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API
    from vkbottle.dispatch import ABCStateDispenser
    from vkbottle.polling import ABCPolling


class UserBlueprint(ABCBlueprint):
    def __init__(
        self,
        name: Optional[str] = None,
        labeler: Optional[UserLabeler] = None,
        router: Optional[Router] = None,
    ):
        if name is not None:
            self.name = name

        self.labeler = labeler or UserLabeler()
        self.router: Router = router or Router()
        self.constructed = False

    def construct(
        self,
        api: Union["ABCAPI", "API"],
        polling: "ABCPolling",
        state_dispenser: "ABCStateDispenser",
        db: Database,
        bot: Bot,
        user: User = None
    ) -> "UserBlueprint":
        self.api = api
        self.polling = polling
        self.state_dispenser = state_dispenser
        self.db = db
        self.bot = bot
        self.constructed = True
        return self

    def load(self, framework: "User") -> "UserBlueprint":
        framework.labeler.load(self.labeler)  # type: ignore
        logger.info("Blueprint {!r} loaded", self.name)
        return self.construct(
            framework.api,
            framework.polling,
            framework.state_dispenser,
            framework.db,
            framework.bot,
        )

    @property
    def on(self) -> UserLabeler:
        return self.labeler
