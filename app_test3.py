from typing import Final  # 引入Final類型，用於定義常量
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot  # 從telegram模組引入Update類
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, \
    ContextTypes  # 從telegram.ext模組引入多個類和模組
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from datetime import datetime, timedelta

TOKEN: Final = '7219739601:AAEYdGgpr4DOxH6YrIKbtm7eCQeXoOCqyTY'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@Concert_info_chat_bot'  # 定義機器人的使用者名稱作為常量

# 创建调度器
scheduler = AsyncIOScheduler()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("start")
    await update.message.reply_text("Welcome! Use /start to begin.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    message = update.message
    user_input: str = update.message.text
    user_id = update.message.chat.id
    print(f'User ({user_id}): "{user_input}"')

    # 初始化查询列表，如果不存在的话
    if 'queries' not in context.user_data:
        context.user_data['queries'] = []

    # 检查是否在等待新查询
    if context.user_data.get('awaiting_new_query'):
        await handle_new_search(update, context, user_input)
    else:
        # 存儲用戶輸入
        context.user_data['queries'].append(user_input)
        await update.message.reply_text(f"{user_input}")

        # 添加選項
        keyboard = [
            [InlineKeyboardButton("Show All", callback_data='show_all')],
            [InlineKeyboardButton("Continue Searching", callback_data='continue_searching')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        print(f"reply_markup = {reply_markup}")
        # await update.message.reply_text('請選擇下一步操作：', reply_markup=reply_markup)
        await update.message.reply_text('Please Choice:', reply_markup=reply_markup)

    # 重置计时器
    reset_timeout(update, context)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == 'show_all':
        queries = context.user_data.get('queries', [])
        await query.edit_message_text(text="Show All Results.")
        await show_all_results(update, context, queries)
        # 繼續之前的查詢邏輯
    elif choice == 'continue_searching':
        await query.edit_message_text(
            text="Please enter a new search keyword. The search mode will end after 30 minutes of inactivity or when you click 'show all':")
        # 等待用戶新的輸入
        context.user_data['awaiting_new_query'] = True

    # 重置计时器
    reset_timeout(update, context)


async def show_all_results(update: Update, context: ContextTypes.DEFAULT_TYPE, concert_indexes):
    # 重置查询列表
    print(f"concert_indexes = {concert_indexes}")
    context.user_data['queries'] = []
    context.user_data['awaiting_new_query'] = False
    await update.callback_query.edit_message_text(text="已顯示所有結果。查詢已重置。")


async def handle_new_search(update: Update, context: ContextTypes.DEFAULT_TYPE, new_query: str):
    context.user_data['queries'].append(new_query)
    await perform_search(update, context, new_query)


async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str):
    # 在這裡執行你的搜索邏輯，例如調用Rasa模型或查詢數據庫
    queries = context.user_data.get('queries', [])
    print(f"queries = {queries}")
    search_results = f"根據您的新關鍵字 '{query}' 和之前的查詢 {queries[:-1]} 進行搜索。"
    await update.message.reply_text(search_results)

    # 添加選項
    keyboard = [
        [InlineKeyboardButton("Show All", callback_data='show_all')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(f"reply_markup = {reply_markup}")
    await update.message.reply_text('or：', reply_markup=reply_markup)


def reset_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    job = context.user_data.get('timeout_job')
    if job:
        job.remove()

    job = scheduler.add_job(
        send_reset_message,
        trigger=IntervalTrigger(seconds=5),
        args=[update, context],
    )
    context.user_data['timeout_job'] = job


async def send_reset_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_new_query'] = False
    context.user_data['queries'] = []
    await update.message.reply_text("Query status has been reset due to 30 minutes of inactivity.")
    job = context.user_data.pop('timeout_job', None)
    if job:
        job.remove()


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    scheduler.start()

    print('Go!')
    app.run_polling(poll_interval=3)
