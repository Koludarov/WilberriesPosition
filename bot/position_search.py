import asyncio
import logging
from typing import Optional, Tuple, Union

import selenium.webdriver.chrome.webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from bot.consts import SORT_T

logger = logging.getLogger(__name__)


async def scroll_to_end(driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """
    Прокручивает страницу до тех пор, пока появляются новые
    карточки товаров. Нужна, чтобы отобразить все товары,
    находящиеся на странице.
    """
    total_article_count = 0
    prev_article_count = 0
    curr_article_count = len(driver.find_elements(By.CSS_SELECTOR, 'article.product-card[data-nm-id]'))
    footer_height = driver.execute_script("return document.querySelector('footer').offsetHeight")

    while curr_article_count > prev_article_count:
        prev_article_count = curr_article_count
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script(f"window.scrollTo(0, {scroll_height - footer_height});")
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
        await asyncio.sleep(0.8)

        driver.execute_script(f"window.scrollTo(0, {scroll_height - footer_height * 2});")
        curr_article_count = len(driver.find_elements(By.CSS_SELECTOR, 'article.product-card[data-nm-id]'))
        new_article_count = curr_article_count - prev_article_count

        total_article_count += new_article_count


async def get_page(url: str) -> Optional[str]:
    """
    Создает запрос через Chrome, с помощью Selenium
    и возвращает ответ
    """
    # Настройка Selenium и ChromeDriver
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        await asyncio.sleep(3)
        await scroll_to_end(driver)
    except WebDriverException as error:
        logger.exception(f'Ошибка Веб драйвера {str(error)[:50]}')
        return None
    except ConnectionError as error:
        logger.exception(f'Ошибка подключения {str(error)[:50]}')
        return None
    except Exception as error:
        logger.exception(f'Ошибка {str(error)[:50]}')
        return None

    html = driver.page_source
    driver.quit()
    return html


async def find_product(
        sort,
        search_query,
        article
) -> Union[Tuple[int, int], Tuple[None, None]]:
    """
    Постранично получает карточки товаров
    и возвращает позицию товара, либо ничего,
    в случаях:
    - Товар с заданным артикулом не был найден
    - Некорректный запрос
    """
    page = 1

    while True:

        logger.info(f'Searching {article} for {search_query} page {page}')
        url = f"https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort={SORT_T[sort]}&search={search_query}"
        response = await get_page(url)
        if not response:
            return None, None
        soup = BeautifulSoup(response, 'html.parser')
        not_found_404 = soup.find('div', class_='content404')
        not_found_element = soup.find('div', class_='catalog-page__not-found not-found-search')
        not_found_element2 = soup.find('div', class_='class="not-found-result')
        if not_found_element or not_found_element2 or not_found_404:
            logger.info(f'Not found {article} for {search_query}')
            return None, None
        product_cards = soup.find_all('article', class_='product-card')
        for product_card in product_cards:
            try:
                article_id = product_card['data-nm-id']
                if article_id == article:
                    logger.info(f'Found {article} page {page}, position {product_cards.index(product_card) + 1}')
                    return page, product_cards.index(product_card) + 1
            except KeyError:
                continue
        page += 1
