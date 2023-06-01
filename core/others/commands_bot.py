from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    """Изменяет команды для бота в специальном меню слева"""
    command = [
        BotCommand(
            command='start',
            description='Начните работу со мной'
        ),
        BotCommand(
            command='cancel',
            description='Если что-то пошло не так'
        )
    ]

    await bot.set_my_commands(command, BotCommandScopeDefault())
