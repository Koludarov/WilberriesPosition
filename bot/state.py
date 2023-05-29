from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchState(StatesGroup):
    """Состояние для поиска товара"""
    waiting_for_sort = State()
    waiting_for_query = State()
    waiting_for_article = State()