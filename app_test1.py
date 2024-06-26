from typing import Final  # 引入Final類型，用於定義常量
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot  # 從telegram模組引入Update類
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, \
    ContextTypes  # 從telegram.ext模組引入多個類和模組
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from datetime import datetime, timedelta

TOKEN: Final = '7219739601:AAEYdGgpr4DOxH6YrIKbtm7eCQeXoOCqyTY'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@Concert_info_chat_bot'  # 定義機器人的使用者名稱作為常量


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("start")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    message = update.message  # to detect reply
    user_input: str = update.message.text  # user input
    user_id = update.message.chat.id
    print(f'User ({user_id}): "{user_input}"')
    await update.message.reply_text(f"{user_input}")

    # 初始化查询列表，如果不存在的话
    if 'queries' not in context.user_data:
        context.user_data['queries'] = []

    # 存儲用戶輸入
    context.user_data['queries'].append(user_input)

    # 添加選項
    keyboard = [
        [InlineKeyboardButton("Show All", callback_data='more')],
        [InlineKeyboardButton("New Search", callback_data='new_search')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(f"reply_markup = {reply_markup}")
    await update.message.reply_text('請選擇下一步操作：', reply_markup=reply_markup)

    # # 檢測是否回覆了某個訊息
    # if update.message.reply_to_message:
    #     replied_message = update.message.reply_to_message.text
    #     update.message.reply_text
    #     update.message.reply_text(f'You replied to: {replied_message}')
    # else:
    #     update.message.reply_text('Please reply to a specific message.')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == 'more':
        await query.edit_message_text(text="顯示更多結果...")
        # await update.message.reply_text(f"111")
        # 繼續之前的查詢邏輯
    elif choice == 'new_search':
        # await update.message.reply_text(f"222")
        await query.edit_message_text(text="請輸入新的查詢關鍵字：")
        # 等待用戶新的輸入
        context.user_data['awaiting_new_query'] = True


async def handle_new_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_new_query'):
        new_query = update.message.text
        context.user_data['awaiting_new_query'] = False
        await perform_search(update, context, new_query)


async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str):
    # 在這裡執行你的搜索邏輯，例如調用Rasa模型或查詢數據庫
    queries = context.user_data.get('queries', [])
    search_results = f"根據您的新關鍵字 '{query}' 和之前的查詢 {queries} 進行搜索。"

    await update.message.reply_text(search_results)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    # app.add_handler(CommandHandler('switch_language', switch_language_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.TEXT, handle_new_search))


    app.add_error_handler(error)

    scheduler = AsyncIOScheduler()
    scheduler.start()

    print('Go!')
    app.run_polling(poll_interval=3)
