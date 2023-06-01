from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    """Изменяет команды для бота в специальном меню слева"""
    command = [
        BotCommand(
            command='Start',
            description='Начните работу со мной'
        ),
        BotCommand(
            command='Cancel',
            description='Если что-то пошло не так'
        ),
        BotCommand(
            command='GitHub',
            description='Ссылка на код бота на Git'
        )
    ]

    await bot.set_my_commands(command, BotCommandScopeDefault())
