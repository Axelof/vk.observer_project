from src.app import user, bot, loop_wrapper
from src.initialize import on_startup
from src.utils import loop


def main():
    loop_wrapper.add_task(user.run_polling())
    loop_wrapper.add_task(bot.run_polling())
    loop_wrapper.add_task(on_startup())  # Если нужно что-то выполнить перед запуском

    loop_wrapper.run_forever(loop=loop)


if __name__ == "__main__":
    main()
