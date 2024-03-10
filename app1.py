from typing import Final  # 引入Final類型，用於定義常量

from telegram import Update  # 從telegram模組引入Update類
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # 從telegram.ext模組引入多個類和模組

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

import asyncio
import re

zh_model = ''  # 把訓練好的中文模型放這裡
en_model = ''  # 把訓練好的英文模型放這裡

TOKEN: Final = '6732658127:AAHc75srUIqqplCdlisn-TeecqlYRyCPUFM'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@kuan_concert_chatbot_test1_bot'  # 定義機器人的使用者名稱作為常量


# 定義三個處理不同指令的異步函式
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Execute start command')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Execute help command')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Execute custom command')


# 根據用戶的訊息內容，回覆不同的訊息
def handle_response(text: str) -> str:
    processed: str = text.lower()

    agent_zh = Agent.load(zh_model)
    agent_en = Agent.load(en_model)
    print('--- 開始 ---')
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
    if bool(chinese_pattern.search(text)):
        result = asyncio.run(agent_zh.parse_message(text))
    else:
        result = asyncio.run(agent_en.parse_message(text))
    print(result)
    print('--- 結束 ---')

    if 'hello' in text:
        return 'Hey there!'

    if 'how are you' in text:
        return 'I am good!'

    if 'i love python' in text:
        return 'I love it too'

    return 'I do not understand what you wrote...'


# 處理用戶發送的訊息，並回覆相應的訊息
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}')  # 印出用戶訊息

    if message_type == 'group':  # 如果是群組訊息
        if BOT_USERNAME in text:  # 如果訊息包含機器人的使用者名稱
            new_text: str = text.replace(BOT_USERNAME, '')  # 去除機器人的使用者名稱
            response: str = handle_response(new_text)  # 根據處理後的訊息回覆
        else:
            return
    else:  # 如果是個人訊息
        response: str = handle_response(text)  # 直接回覆

    print('Bot:', response)  # 印出機器人的回覆
    await update.message.reply_text(response)  # 回覆用戶的訊息


# 處理錯誤的異步函式
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')  # 印出錯誤訊息


if __name__ == '__main__':
    print('Starting bot...')  # 印出機器人啟動訊息
    app = Application.builder().token(TOKEN).build()  # 建立Telegram應用程式實例

    # 添加處理不同指令的處理器
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))  # 添加處理文字訊息的處理器

    app.add_error_handler(error)  # 添加處理錯誤的處理器

    print('Polling...')  # 印出輪詢訊息
    app.run_polling(poll_interval=3)  # 開始輪詢，設定輪詢間隔為3秒
