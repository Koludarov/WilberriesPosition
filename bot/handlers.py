import logging

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.loader import dp
from bot.position_search import find_product
from bot.state import SearchState
from bot.utils import contains_only_digits

logger = logging.getLogger(__name__)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """
    Отправляет приветственное сообщение.
    """
    await message.reply("""Привет! Отправь мне поисковый запрос и артикул, чтобы найти товар на Wildberries.
    \nДля старта воспользуйтесь командой:  /search""")


@dp.message_handler(Command("cancel"), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Отменяет текущее состояние
    """
    await state.finish()
    await message.reply("Операция отменена.")


@dp.message_handler(commands=['search'])
async def sort_handler(message: types.Message):
    """
    Обрабатывает команду /search и запускает состояние.
    """
    await SearchState.waiting_for_sort.set()
    await message.reply("""Выберите сортировку поисковой выдачи:
    \n1 - По популярности\n2 - По рейтингу\n3 - По возрастанию цены
4 - По убыванию цены\n5 - По новинкам\n6 - Сначала выгодные""")


@dp.message_handler(state=SearchState.waiting_for_sort)
async def process_sort(message: types.Message, state: FSMContext):
    """
    Записывает метод сортировки поиска.
    """
    sort_method = message.text.strip()
    error_message = "Ответ должен быть цифрой от 1 до 6"
    if not sort_method.isdigit():
        await message.reply(error_message)
        return
    else:
        if int(sort_method) not in range(1, 7):
            await message.reply(error_message)
            return
    await state.update_data(sort_method=sort_method)
    await SearchState.next()
    await message.reply("Отправьте поисковый запрос (название товара):")


@dp.message_handler(state=SearchState.waiting_for_query)
async def process_query(message: types.Message, state: FSMContext):
    """
    Записывает поисковый запрос.
    """
    search_query = message.text.strip()
    await state.update_data(search_query=search_query)
    await SearchState.next()
    await message.reply("Отправьте артикул товара:")


@dp.message_handler(state=SearchState.waiting_for_article)
async def process_article(message: types.Message, state: FSMContext):
    """
    Записывает артикул для поиска. Передаёт поисковой функции и
    возвращается с ответом к пользователю.
    """
    article = message.text.strip()
    if not contains_only_digits(article):
        await message.reply("Артикул должен состоять из цифр")
        return
    search_query_data = await state.get_data()
    search_query = search_query_data.get('search_query')
    sort_method = search_query_data.get('sort_method')
    await message.reply("""Начинаю поиск товара.\nЭто займёт какое-то время
    \nДля отмены поиска воспользуйтесь командой - /cancel""")
    page_number, position = await find_product(sort_method, search_query, article)

    if page_number is not None and position is not None:
        response_message = f"Артикул {article} найден на странице {page_number}, место на странице: {position}"
    else:
        response_message = f"Артикул {article} не найден."

    await message.reply(response_message)
    await state.finish()


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    """
    Отправляет сообщение со списком доступных команд бота.
    """
    help_text = "Список доступных команд:\n"
    help_text += "/start - начать использование бота\n"
    help_text += "/help - получить список доступных команд\n"
    help_text += "/search - запрос поиска позиции товара\n"
    help_text += "/cancel - команда для отмены действия\n"
    await message.answer(help_text)
