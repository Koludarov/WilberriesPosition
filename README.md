# WilberriesPosition
WilberriesPosition - это Telegram-бот, который позволяет искать позицию товара на странице поисковой системы Wilberries. Бот использует Selenium WebDriver для автоматизации поиска и анализа результатов.

## Требования
Для работы WilberriesPosition вам понадобятся следующие компоненты:
1 - Вариант запуска
* Python 3.x (установленный на вашей системе)
* Браузер Google Chrome (установленный на вашей системе)

2 - Вариант запуска
* Docker
* Docker Compose

Установка
Клонируйте репозиторий WilberriesPosition:

```bash
git clone https://github.com/Koludarov/WilberriesPosition.git
```
Перейдите в каталог проекта:

```bash
cd WilberriesPosition
```

Конфигурация

Откройте файл .env в текстовом редакторе и добавьте следующие переменные окружения:

```dotenv
TELEGRAM_BOT_TOKEN=<your_bot_token>
```
Замените <your_bot_token> на токен, полученный от BotFather при создании Telegram-бота.

## Запуск с использованием Docker Compose
Убедитесь, что у вас установлен Docker и Docker Compose.

В корневом каталоге проекта выполните следующую команду:


```bash
docker-compose up
```
Это запустит контейнеры для бота и Selenium Grid.

## Запуск с использованием Python

Cоздайте виртуальное окружение и установите зависимости, используя pip:


```bash
# Создание виртуального окружения
python -m venv myenv
```
```bash
# Активация виртуального окружения на Windows
myenv\Scripts\activate
```
```bash
# Активация виртуального окружения на macOS и Linux
source myenv/bin/activate
```
```bash
pip install -r requirements.txt
```

В корневом каталоге проекта выполните следующую команду:


```bash
python -m bot
```
Это запустит бота без использования Docker и Selenium Grid. Убедитесь, что у вас установлен Python и Chrome на вашей системе.

## Использование
Найдите бота в Telegram по его имени или токену.

Введите команду `/start`, чтобы начать использование бота.

Введите команду `/search`, чтобы начать поиск.

Бот будет запрашивать у вас поисковый запрос и сортировку результатов.

После ввода запроса и сортировки бот выполнит поиск на Wilberries и сообщит вам о позиции товара на странице.

Для отмены запроса, используйте команду `/cancel`

## Вклад и отзывы
Проект WilberriesPosition открыт для вклада и отзывов. Если у вас есть предложения по улучшению функциональности, найденные ошибки или другие вопросы, пожалуйста, создайте Issue в репозитории на GitHub.

## Лицензия
Проект распространяется под лицензией <a href="https://github.com/Koludarov/WilberriesPosition/blob/main/LICENSE">MIT License</a>.