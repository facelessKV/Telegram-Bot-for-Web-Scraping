import logging
import asyncio
import re
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Загружаем переменные окружения для безопасного хранения токена
load_dotenv()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменной окружения
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Для хранения состояний пользователей
dp = Dispatcher(storage=storage)

# Словарь для хранения URL для каждого пользователя
user_urls = {}

# Определение состояний для FSM (Finite State Machine)
class Form(StatesGroup):
    waiting_for_url = State()  # Состояние ожидания URL от пользователя

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    """
    Обработчик команды /start
    Отправляет приветственное сообщение и краткую инструкцию
    """
    await message.reply(
        "Привет! Я бот для парсинга веб-сайтов.\n"
        "Используйте /set_url для установки URL сайта,\n"
        "затем /parse для получения данных с сайта.\n"
        "Введите /help для получения подробной инструкции."
    )

# Обработчик команды /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    """
    Обработчик команды /help
    Отправляет подробную инструкцию по использованию бота
    """
    help_text = (
        "📌 *Инструкция по использованию бота*\n\n"
        "*Доступные команды:*\n"
        "/set_url - установить URL сайта для парсинга\n"
        "/parse - выполнить парсинг данных с установленного URL\n"
        "/help - показать эту инструкцию\n\n"
        "*Как пользоваться:*\n"
        "1. Отправьте команду /set_url\n"
        "2. Введите полный URL сайта (включая http:// или https://)\n"
        "3. После установки URL, используйте команду /parse для получения данных\n\n"
        "*Примечание:* Бот извлекает основной текстовый контент со страницы. "
        "Для некоторых сайтов могут быть ограничения на парсинг."
    )
    await message.reply(help_text, parse_mode="MarkdownV2")

# Обработчик команды /set_url
@dp.message(Command("set_url"))
async def set_url_command(message: types.Message, state: FSMContext):
    """
    Обработчик команды /set_url
    Переводит пользователя в состояние ожидания URL
    """
    await state.set_state(Form.waiting_for_url)
    await message.reply("Пожалуйста, введите URL сайта для парсинга:")

# Обработчик получения URL от пользователя
@dp.message(Form.waiting_for_url)
async def process_url(message: types.Message, state: FSMContext):
    """
    Обработчик получения URL от пользователя
    Проверяет корректность URL и сохраняет его для пользователя
    """
    url = message.text.strip()
    
    # Проверка на корректность URL (базовая валидация)
    url_pattern = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    if not url_pattern.match(url):
        await message.reply(
            "Некорректный URL. Пожалуйста, убедитесь, что URL начинается с http:// или https://"
        )
        return

    # Сохраняем URL для данного пользователя
    user_id = message.from_user.id
    user_urls[user_id] = url
    
    await state.clear()  # Выходим из состояния ожидания URL
    await message.reply(f"URL успешно установлен: {url}")

# Обработчик команды /parse
@dp.message(Command("parse"))
async def parse_command(message: types.Message):
    """
    Обработчик команды /parse
    Выполняет парсинг сайта по сохраненному URL пользователя
    """
    user_id = message.from_user.id
    
    # Проверяем, установлен ли URL для данного пользователя
    if user_id not in user_urls:
        await message.reply(
            "URL не установлен. Пожалуйста, используйте команду /set_url для установки URL."
        )
        return
    
    url = user_urls[user_id]
    await message.reply(f"Начинаю парсинг сайта: {url}\nЭто может занять некоторое время...")
    
    try:
        # Парсинг сайта
        parsing_result = await parse_website(url)
        
        # Если результат слишком длинный, разбиваем его на части
        if len(parsing_result) > 4000:
            chunks = [parsing_result[i:i+4000] for i in range(0, len(parsing_result), 4000)]
            for i, chunk in enumerate(chunks):
                await message.reply(f"Часть {i+1}/{len(chunks)}:\n\n{chunk}")
        else:
            await message.reply(parsing_result)
            
    except Exception as e:
        await message.reply(f"Произошла ошибка при парсинге сайта: {str(e)}")

async def parse_website(url):
    """
    Функция для парсинга веб-сайта
    
    Args:
        url (str): URL сайта для парсинга
        
    Returns:
        str: Результат парсинга (текстовое содержимое сайта)
    """
    # Устанавливаем User-Agent, чтобы сайт принял наш запрос
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Отправляем GET-запрос на указанный URL
    response = requests.get(url, headers=headers, timeout=10)
    
    # Проверяем успешность запроса
    response.raise_for_status()
    
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Удаляем все скрипты и стили, так как они не содержат полезной текстовой информации
    for script in soup(["script", "style"]):
        script.extract()
    
    # Извлекаем основной текст страницы
    text = soup.get_text()
    
    # Очищаем текст от лишних пробелов и пустых строк
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    # Если текст слишком длинный, обрезаем его
    if len(text) > 15000:
        text = text[:15000] + "...\n[Текст обрезан из-за большого размера]"
    
    # Добавляем базовую информацию о странице
    title = soup.title.string if soup.title else "Без заголовка"
    
    # Находим все ссылки на странице
    links = soup.find_all('a', href=True)
    links_text = "\n".join([f"- {link.get_text(strip=True)} ({link['href']})" 
                          for link in links[:10] if link.get_text(strip=True)])
    
    if len(links) > 10:
        links_text += f"\n... и еще {len(links) - 10} ссылок"
    
    # Формируем итоговый результат
    result = f"📄 *Заголовок страницы:* {title}\n\n"
    result += f"🔗 *Основные ссылки:*\n{links_text}\n\n"
    result += f"📝 *Текстовое содержимое:*\n{text[:4000]}"
    
    if len(text) > 4000:
        result += "\n...\n[Показана только часть текста]"
    
    return result

# Обработчик для всех остальных сообщений
@dp.message(F.text)
async def echo(message: types.Message):
    """
    Обработчик для всех остальных сообщений
    Отправляет подсказку о доступных командах
    """
    await message.reply(
        "Я не понимаю эту команду. Используйте:\n"
        "/set_url - для установки URL\n"
        "/parse - для парсинга сайта\n"
        "/help - для получения инструкции"
    )

# Точка входа
async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск бота
    asyncio.run(main())