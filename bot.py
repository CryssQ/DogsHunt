import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F

API_TOKEN = '7898974668:AAGVtegAHJzPxhdD8k_eE6VYB3kKJd-I6qI'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

start_button = KeyboardButton(text="🕹️ Start Hunter")
stop_button = KeyboardButton(text="⏹️ Stop Hunter")
keyboard = ReplyKeyboardMarkup(keyboard=[[start_button, stop_button]], resize_keyboard=True)

timer_running = False
task = None

async def remind_user(chat_id):
    await bot.send_message(chat_id, "⏰ Hey! Time's up! Come into the game quickly! 🚀\n\n"
                                    "👉 Click the link to join: https://t.me/dogshouse_bot/join?startapp=lWyveYSWT4C_oQjI9Y0BNw .", reply_markup=keyboard)

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    welcome_message = (
        "👋 Hello, welcome to the Hunter bot! 🕹️\n\n"
        "🎮 We'll help you collect all the rewards in DOGS! 🐶\n\n"
        "⏳ Set a timer for 24 hours, and we'll remind you!⏰\n\n"
        "💸 Also, if it's not too much trouble, you can support us by sending some tokens to our wallet address: 💰\n\n"
        f"<code>UQCddMiB2nGniPP63JRn8MLqPLA9f7hxR7GP0GKqgOlZBP5H</code>\n\n"
        "✨ Click on '🕹️ Start Hunter' to start hunting!"
    )
    await message.answer(welcome_message, reply_markup=keyboard, parse_mode="HTML")

@dp.message(F.text == "🕹️ Start Hunter")
async def start_timer(message: types.Message):
    global timer_running, task

    if timer_running:
        await message.answer("🚨 We're already hunting!! 🎯")
        return

    async def timer():
        await asyncio.sleep(60*60*24)
        await remind_user(message.chat.id)

    task = asyncio.create_task(timer())
    timer_running = True
    await message.answer("🎯 Let's go hunting! 🏹\n\n"
                         "⏳ We will notify you in 24 hours. Stay tuned! ⚡️", reply_markup=keyboard)

@dp.message(F.text == "⏹️ Stop Hunter")
async def stop_timer(message: types.Message):
    global timer_running, task

    if not timer_running:
        await message.answer("😅 We haven't gone hunting yet!")
        return

    task.cancel()
    timer_running = False
    await message.answer("🛑 Hunt stopped. You can always start it again!", reply_markup=keyboard)

@dp.errors()
async def error_handler(update: types.Update, exception: Exception):
    logger.error(f"Error processing update {update}: {exception}")
    if isinstance(exception, Exception):
        await bot.send_message(update.message.chat.id, "⚠️ An error occurred, please contact the administrator: @cryssq..")
    return True

async def on_start():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(on_start())
