from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class InfoMiddleware(BaseMiddleware[Message]):
    async def post(self):
        if not self.handlers:
            self.stop("Сообщение не было обработано")

        print(
            "Сообщение было обработано:\n\n"
            f"View - {self.view}\n\n"
            f"Handlers - {self.handlers}"
        )