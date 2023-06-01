from aiogram import Dispatcher, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from core.others.aiohttp_parser import get_info
from core.keyboards.keyboards import accept_kb


class ArticleSearch(StatesGroup):
    """
    Состояния для всех текущих хэндлеров
    """
    await_product_group = State()
    await_product_article = State()
    await_parsing = State()


async def start_command(message: Message, state: FSMContext):
    """
    Хэндлер для старта. Осуществляет переход к первому стейту
    """
    await state.set_state(ArticleSearch.await_product_group)
    msg = await message.answer(
        'Данил Георгиевич, доброго времени суток!👋'
        '\n\nЧтобы узнать позицию отправьте мне сначала название группы товаров где будем искать')
    await state.update_data(
        msg_id=msg.message_id,
        chat_id=msg.chat.id
    )


async def get_product_group(message: Message, state: FSMContext, bot: Bot):
    """
    Сохранение названия групп товаров и переход к подтверждению верности введенных данных
    """
    await state.update_data(group=message.text.lower())
    await message.delete()
    all_data = await state.get_data()
    await bot.edit_message_text(
        chat_id=all_data['chat_id'],
        message_id=all_data['msg_id'],
        text=f'🔎 <b>{message.text}</b> - эту группу товаров ищем?'
             '\nВыберите да или нет на клавиатуре ниже',
        reply_markup=accept_kb,
        parse_mode='HTML'
    )


async def get_accept_product_group(call: CallbackQuery, state: FSMContext):
    """
    Проверка верности ответа, если нет, переход к статусу получения имени группы,
    если верно, то запрос артикула и переход к следующему стэйту
    """
    if call.data == 'yes':
        all_data = await state.get_data()
        await state.set_state(ArticleSearch.await_product_article)
        await call.message.edit_text(
            text=f'🔎 Ищем <b>{all_data["group"]}</b>'
                 f'\n\n🗄 Теперь введите артикул товара для поиска',
            reply_markup=None,
            parse_mode='HTML'
        )
    else:
        await call.message.edit_text(
            text=f'🔎 Повторно введите название группы товаров, где будем искать.'
                 f'\n\nПросто отправьте мне <b>текстом</b> название группы товаров',
            reply_markup=None,
            parse_mode='HTML'
        )


async def get_product_article(message: Message, state: FSMContext, bot: Bot):
    """
    Сохранение артикула и запрос верно ли он указан
    """
    all_data = await state.get_data()
    await message.delete()
    try:
        await state.update_data(article=int(message.text))

        await bot.edit_message_text(
            chat_id=all_data['chat_id'],
            message_id=all_data['msg_id'],
            text=f'🔎 В группе <b>{all_data["group"]}</b>'
                 f'\nИщем <b>{message.text}</b> - именно такой артикул?'
                 '\n\nВыберите да или нет на клавиатуре ниже',
            reply_markup=accept_kb,
            parse_mode='HTML'
        )
    except ValueError:

        await bot.edit_message_text(
            chat_id=all_data['chat_id'],
            message_id=all_data['msg_id'],
            text=f'❌❌❌ {message.text} - это не похоже на артикул число'
                 f'\n\nОбязательно отправьте именно <b>число</b>',
            reply_markup=None,
            parse_mode='HTML'
        )


async def get_accept_product_article(call: CallbackQuery, state: FSMContext):
    """
    Финальный хэндлер, если выбрано, что артикул неверен, то возврат к соответствующему стейту,
    если артикул верен, то происходит парсинг данных товаров через aiohttp.
    После получения данных вывод соответствующего сообщения
    """
    all_data = await state.get_data()
    if call.data == 'yes':
        await state.set_state(ArticleSearch.await_parsing)
        article = all_data['article']
        await call.message.edit_text(
            '‼️ Подождите, осуществляем парсинг'
            '\n\nПарсинг сделал асинхронным, поэтому запрашиваем сразу 50 первых страниц'
            '\n\nА пока можете убедиться, что ищете верный артикул:'
            f'\n🗄 Группа поиска: <b>{all_data["group"]}</b>'
            f'\n🆔 Артикул: <b>{all_data["article"]}</b>'
            f'\n<b><a href="https://www.wildberries.ru/catalog/{article}/detail.aspx">Ссылка на товар</a></b>',
            parse_mode='HTML'
        )

        info = await get_info(
            products_group=all_data['group'],
            article=all_data['article']
        )

        if not info:
            await call.message.answer(f'В первых 5000 позиций данный артикул не найден'
                                      f'\nЯ не делал авто повтор, поэтому придется повторить процедуру снова')

        else:
            await call.message.answer(
                f'🗄 Группа поиска: <b>{all_data["group"]}</b>'
                f'\n🆔 Артикул: <b>{all_data["article"]}</b>'
                f'\n<b><a href="https://www.wildberries.ru/catalog/{all_data["article"]}/detail.aspx">Ссылка на товар</a></b>'
                f'\n\n‼️ НАЙДЕН НА СТРАНИЦЕ(по 100 объектов) - <b>{info["page"]}</b>'
                f'\nпозиция на странице - <b>{info["position on the page"]}</b>',
                parse_mode='HTML'
            )
    else:
        await call.message.edit_text(
            text=f'🔎 Повторно введите артикул товара на wildberries, который будем искать.'
                 f'\n🔎 В группе <b>{all_data["group"]}</b>'
                 f'\n\nПросто отправьте мне <b>числом</b> артикул',
            reply_markup=None,
            parse_mode='HTML'
        )


def handlers_for_search(dp: Dispatcher) -> None:
    """
    Регистрация хэндлеров для дальнейшего импорта в бота
    """
    dp.message.register(start_command, commands=['start', 'старт'])
    dp.message.register(get_product_group, state=ArticleSearch.await_product_group)
    dp.callback_query.register(get_accept_product_group, state=ArticleSearch.await_product_group)
    dp.message.register(get_product_article, state=ArticleSearch.await_product_article),
    dp.callback_query.register(get_accept_product_article, state=ArticleSearch.await_product_article)
