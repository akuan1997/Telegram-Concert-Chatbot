from typing import Final
import threading  # 引入threading模組

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import time

TOKEN: Final = 'YOUR_TOKEN_HERE'
BOT_USERNAME: Final = '@YOUR_BOT_USERNAME_HERE'

user_language_preferences = {}
user_status = {}
user_language_file = "user_preferred_language.txt"

def get_user_language(id):
    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if id in line:
            return line[line.index('|||') + 3:line.index('|||') + 5]

# 定義三個處理不同指令的異步函式
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = f"""
歡迎！ 請選擇你偏好的語言。
輸入1 (中文)
輸入2 (英文)
語言可以隨時在左下角的menu當中選擇切換。
如果沒有輸入我們將使用預設語言: 中文

Welcome! Please choose your preferred language.
Enter 1 (Chinese)
Enter 2 (English)
You can always switch languages in the menu at the bottom left.
If no input is provided, we will use the default language: Chinese.
"""
    await update.message.reply_text(txt)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Execute help command')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    user_status[user_id] = ""
    print(user_status)
    await update.message.reply_text(str(user_id))
    await update.message.reply_text('Execute custom aaa command')

async def switch_language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if str(update.message.chat.id) in line:
            if 'zh' in line:
                lines[i] = line.replace('zh', 'en')
                await update.message.reply_text("No problem! Your preferred language has been set to English!")
            else:
                lines[i] = line.replace('en', 'zh')
                await update.message.reply_text("沒問題! 你的偏好語言已設定為中文!")
            with open(user_language_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            break

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in text:
        return 'Hey there!'

    if 'how are you' in text:
        return 'I am good!'

    if 'i love python' in text:
        return 'I love it too'

    return 'I do not understand what you wrote...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user_id = update.message.chat.id
    print(f'User ({user_id}) in {message_type}: "{text}"')

    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.replace('\n', '').split('|||')[0] for line in lines]
    print('handle message', lines)

    if str(user_id) in lines:
        if get_user_language(str(user_id)) == 'zh':
            response: str = handle_response(text)
            print('Bot:', response)
            await update.message.reply_text('現在就由我鎖鏈安妮當你的對手')
        else:
            response: str = handle_response(text)
            print('Bot:', response)
            await update.message.reply_text('Never gonna give you up')

    elif text.strip() in ('1', '2'):
        user_language_preferences[user_id] = 'Chinese' if text.strip() == '1' else 'English'
        if user_language_preferences[user_id] == 'Chinese':
            await update.message.reply_text("沒問題! 你的偏好語言已設定為中文!")
            with open(user_language_file, 'a', encoding='utf-8') as f:
                f.write(f"{user_id}|||zh\n")
        else:
            await update.message.reply_text("No problem! Your preferred language has been set to English!")
            with open(user_language_file, 'a', encoding='utf-8') as f:
                f.write(f"{user_id}|||en\n")
    else:
        await update.message.reply_text("請先設置語言!\nPlease set the language first!")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def get_latest_info(filename):
    while True:
        # 實現你要執行的功能，這裡用打印代替
        print(f"Reading latest info from {filename}")
        time.sleep(10)  # 模擬間隔時間

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('switch_language', switch_language_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    # 創建一個新的線程來執行get_latest_info
    info_thread = threading.Thread(target=get_latest_info, args=("filename.txt",))
    info_thread.start()

    print('Polling...')
    app.run_polling(poll_interval=3)
