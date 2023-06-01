from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

accept_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='✅ Да',
                        callback_data='yes'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='❌ Нет',
                        callback_data='no'
                    )
                ]
            ]
        )
