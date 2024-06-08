from typing import Final  # 引入Final類型，用於定義常量
from telegram import Update, Bot  # 從telegram模組引入Update類
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # 從telegram.ext模組引入多個類和模組
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import random

TOKEN: Final = '7219739601:AAEYdGgpr4DOxH6YrIKbtm7eCQeXoOCqyTY'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@Concert_info_chat_bot'  # 定義機器人的使用者名稱作為常量
# 隨機字串列表
random_strings = [
    "Hello, how are you?",
    "What's your favorite color?",
    "Do you like music?",
    "What's your favorite movie?",
    "Tell me something interesting!"
]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 發送幾個隨機字串訊息
    for _ in range(3):  # 發送三個隨機字串
        message = random.choice(random_strings)
        update.message.reply_text(message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 檢測是否回覆了某個訊息
    if update.message.reply_to_message:
        replied_message = update.message.reply_to_message.text
        update.message.reply_text(f'You replied to: {replied_message}')
    else:
        update.message.reply_text('Please reply to a specific message.')