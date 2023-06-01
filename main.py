import asyncio
import logging

from aiogram import Bot

from core.others.commands_bot import set_commands
from core.others.create_bot import dp, bot
from core.handlers.find_article import handlers_for_search
from core.others.settings import settings

logger = logging.getLogger(__name__)


async def start_bot(bot: Bot):
    """Функция исполняемая при старте бота
    меняет команды в меню бота"""
    await set_commands(bot)
    await bot.send_message(settings.user.admin_id, text='Bot started')


async def start():
    """Функция старта бота с регистрацией хендлеров и других частей, потом явно будут мидлвари"""
    logging.basicConfig(
        level=logging.INFO
    )

    dp.startup.register(start_bot)

    handlers_for_search(dp)

    await dp.start_polling(bot, polling_timeout=100)
    await dp.we

if __name__ == '__main__':
    asyncio.run(start())
