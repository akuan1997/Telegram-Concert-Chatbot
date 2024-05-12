# https://www.youtube.com/watch?v=vZtm1wuA2yc&t=1183s&ab_channel=Indently
from typing import Final  # 引入Final類型，用於定義常量

from telegram import Update  # 從telegram模組引入Update類
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # 從telegram.ext模組引入多個類和模組

TOKEN: Final = '6732658127:AAHc75srUIqqplCdlisn-TeecqlYRyCPUFM'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@kuan_concert_chatbot_test1_bot'  # 定義機器人的使用者名稱作為常量

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
            # print(lines)
            with open(user_language_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            break


# 根據用戶的訊息內容，回覆不同的訊息
def handle_response(text: str) -> str:
    processed: str = text.lower()

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
    user_id = update.message.chat.id
    print(f'User ({user_id}) in {message_type}: "{text}"')  # 印出用戶訊息

    # if message_type == 'group':  # 如果是群組訊息
    #     if BOT_USERNAME in text:  # 如果訊息包含機器人的使用者名稱
    #         new_text: str = text.replace(BOT_USERNAME, '')  # 去除機器人的使用者名稱
    #         response: str = handle_response(new_text)  # 根據處理後的訊息回覆
    #     else:
    #         return
    # else:  # 如果是個人訊息
    # response: str = handle_response(text)  # 直接回覆

    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.replace('\n', '').split('|||')[0] for line in lines]
    print('handle message', lines)

    if str(user_id) in lines:  # 使用者已經選擇語言
        if get_user_language(str(user_id)) == 'zh':
            response: str = handle_response(text)  # 直接回覆
            print('Bot:', response)  # 印出機器人的回覆
            # await update.message.reply_text(response)  # 回覆用戶的訊息
            await update.message.reply_text('現在就由我鎖鏈安妮當你的對手')  # 回覆用戶的訊息
        else:
            response: str = handle_response(text)  # 直接回覆
            print('Bot:', response)  # 印出機器人的回覆
            # await update.message.reply_text(response)  # 回覆用戶的訊息
            await update.message.reply_text('Never gonna give you up')  # 回覆用戶的訊息


    elif text.strip() in ('1', '2'):  # 使用者還沒選擇語言
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
    app.add_handler(CommandHandler('switch_language', switch_language_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))  # 添加處理文字訊息的處理器

    app.add_error_handler(error)  # 添加處理錯誤的處理器

    print('Polling...')  # 印出輪詢訊息
    app.run_polling(poll_interval=3)  # 開始輪詢，設定輪詢間隔為3秒
