from typing import Final  # 引入Final類型，用於定義常量
from telegram import Update, Bot  # 從telegram模組引入Update類
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # 從telegram.ext模組引入多個類和模組
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from fuzzywuzzy import fuzz
import yaml
import re

TOKEN: Final = '7219739601:AAEYdGgpr4DOxH6YrIKbtm7eCQeXoOCqyTY'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@Concert_info_chat_bot'  # 定義機器人的使用者名稱作為常量
user_language_file = "user_preferred_language.txt"


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


def get_user_language(id):
    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if id in line:
            return line[line.index('|||') + 3:line.index('|||') + 5]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    user_id = update.message.chat.id
    print(f"user ID = {user_id}")

    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.replace('\n', '').split('|||')[0] for line in lines]
    # print('handle message', lines)

    if str(user_id) in lines:
        if get_user_language(str(user_id)) == 'zh':
            print('chinese')
            if message.reply_to_message:
                reply_message = message.reply_to_message
                reply_text = reply_message.text
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"你回覆的訊息是: {reply_text}")  # test
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="你沒有回覆訊息")  # test
        else:
            print('english')
            if message.reply_to_message:
                reply_message = message.reply_to_message
                reply_text = reply_message.text
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Replied to: {reply_text}")  # test
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="This is not a reply msg")  # test


#
#     with open(user_language_file, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#     lines = [line.replace('\n', '').split('|||')[0] for line in lines]
#     print('handle message', lines)
#
#     if str(user_id) in lines:
#         if get_user_language(str(user_id)) == 'zh':
#             found_indexes = await get_zh_indexes(text, zh_json)
#             messages = show_concert_info(found_indexes, 'zh')
#         else:
#             found_indexes = await get_en_indexes(text, en_json)
#             messages = show_concert_info(found_indexes, 'en')
#
#         print(f"一共找到{len(found_indexes)}筆資料")
#         for msg in messages:
#             await update.message.reply_text(msg)
#
#     elif text.strip() in ('1', '2'):
#         user_language_preferences[user_id] = 'Chinese' if text.strip() == '1' else 'English'
#         if user_language_preferences[user_id] == 'Chinese':
#             txt = """
# 沒問題! 你的偏好語言已設定為中文!
#
# ---
#
# 你可以通過歌手名稱、音樂類型、城市或特定時間來查詢即將舉行的音樂會
# 示例輸入：
# "周杰倫"
# "饒舌"
# "台北"
# "明天"
#
# 你也可以同時指定多個條件
# 範例：
# "蔡依林在台北的音樂會"
# "Post Malone，下個月"
# "嘻哈，這周，台南"
#
# 此外，你還可以查詢即將開始售票的音樂會
# 範例：
# "查找明天開始售票的音樂會"
# "售票時間，今天和明天"
#
# 祝您演唱會玩得開心！
# """
#             await update.message.reply_text(txt)
#             with open(user_language_file, 'a', encoding='utf-8') as f:
#                 f.write(f"{user_id}|||zh\n")
#         else:
#             txt = """
# No problem! Your preferred language has been set to English!
#
# ---
#
# Usage Instructions:
#
# You can inquire upcoming concerts by artist name, genre, city, or specific time.
# Example inputs:
# "Taylor Swift"
# "Rap"
# "Taipei"
# "Tomorrow"
#
# You can also specify multiple criteria simultaneously.
# Example inputs:
# "Taylor Swift concerts in Taipei"
# "Post Malone, next month"
# "Hip-Hop, this week, and in Tainan city"
#
# Further more, you can inquire which concerts are going to start selling the tickets.
# Example inputs:
# "Find out which concerts are open for sale tomorrow"
# "Ticketing time, today and tomorrow"
#
# Have Fun!
# """
#             await update.message.reply_text(txt)
#             with open(user_language_file, 'a', encoding='utf-8') as f:
#                 f.write(f"{user_id}|||en\n")
#     else:
#         await update.message.reply_text("請先設置語言!\nPlease set the language first!")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    user_id = update.message.chat.id
    if get_user_language(str(user_id)) == 'zh':
        await app.bot.send_message(chat_id=user_id, text="對不起，我不太理解。")
    else:
        await app.bot.send_message(chat_id=user_id, text="Sorry, I don't understand.")


# async def send_daily_update():
#     with open(user_language_file, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#
#     zh_texts = ['中文1', '中文2']
#     en_texts = ['eng1', 'eng2']
#     for line in lines:
#         user_id, language = line.strip().split('|||')
#         user_id = int(user_id)
#         if language == 'zh':
#             msgs = await get_daily_msg('zh')
#             for msg in msgs:
#                 await app.bot.send_message(chat_id=user_id, text=msg)
#         else:
#             msgs = await get_daily_msg('en')
#             for msg in msgs:
#                 await app.bot.send_message(chat_id=user_id, text=msg)


# def check_if_today(text):
#     pattern = r"concert_(\d{1,2})_(\d{1,2})_(\d{1,2}).json"
#     month_day = re.search(pattern, text)
#     month = int(month_day.group(1))
#     day = int(month_day.group(2))
#
#     # print(month, datetime.now().month)
#     # print(day, datetime.now().day)
#     if month == datetime.now().month and day == datetime.now().day:
#         return True
#     else:
#         return False


# async def get_daily_msg(language):
#     new_file = get_latest_json_filename("new_concerts")
#     plus_file = get_latest_json_filename("plus_concerts")
#
#     if not (check_if_today(new_file) or check_if_today(plus_file)):
#         if language == 'zh':
#             formatted_str_list = ["今天沒有任何的資訊"]
#         else:
#             formatted_str_list = ["The is no information today."]
#
#         print('no new file and no plus file')
#         return formatted_str_list
#
#     # data = read_json(json_filename)
#     # pins = [item['pin'] for item in data]
#     #
#     # pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in pins]
#
#     formatted_str_list = []
#
#     if language == 'zh':
#         zh_data = read_json("concert_zh.json")
#
#         if check_if_today(new_file):
#             new_data = read_json(f"new_concerts/{new_file}")
#             new_pins = [item['pin'] for item in new_data]
#             new_pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in new_pins]
#
#             formatted_str_list.append('新的演唱會資訊!')
#             for index in new_pin_indexes:
#                 concert = zh_data[index]
#
#                 if concert['prc']:
#                     sorted_prices = sorted(concert['prc'], reverse=True)
#                     sorted_prices_str = ', '.join(map(str, sorted_prices))
#                 else:
#                     sorted_prices_str = '-'
#                 concert_date_str = ', '.join(concert['pdt'])
#
#                 if concert['sdt']:
#                     sale_date_str = ', '.join(concert['sdt'])
#                 else:
#                     sale_date_str = '-'
#
#                 if concert['loc']:
#                     location_str = ', '.join(concert['loc'])
#                 else:
#                     location_str = '-'
#
#                 formatted_str = f"""
# - {concert['tit']}
# - 售票日期: {sale_date_str}
# - 表演日期: {concert_date_str}
# - 票價: {sorted_prices_str}
# - 地點: {location_str}
# {concert['url']}
#                                         """
#                 formatted_str_list.append(formatted_str.strip())
#
#         if check_if_today(plus_file):
#             plus_data = read_json(f"plus_concerts/{plus_file}")
#             plus_pins = [item['pin'] for item in plus_data]
#             plus_pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in plus_pins]
#
#             formatted_str_list.append('新的加場資訊!')
#             for index in plus_pin_indexes:
#                 concert = zh_data[index]
#
#                 if concert['prc']:
#                     sorted_prices = sorted(concert['prc'], reverse=True)
#                     sorted_prices_str = ', '.join(map(str, sorted_prices))
#                 else:
#                     sorted_prices_str = '-'
#
#                 concert_date_str = ', '.join(concert['pdt'])
#
#                 if concert['sdt']:
#                     sale_date_str = ', '.join(concert['sdt'])
#                 else:
#                     sale_date_str = '-'
#
#                 if concert['loc']:
#                     location_str = ', '.join(concert['loc'])
#                 else:
#                     location_str = '-'
#
#                 formatted_str = f"""
# - {concert['tit']}
# - 售票日期: {sale_date_str}
# - 表演日期: {concert_date_str}
# - 票價: {sorted_prices_str}
# - 地點: {location_str}
# {concert['url']}
#                                                     """
#                 formatted_str_list.append(formatted_str.strip())
#
#     if language == 'en':
#         en_data = read_json("concert_en.json")
#
#         if check_if_today(new_file):
#             new_data = read_json(f"new_concerts/{new_file}")
#             new_pins = [item['pin'] for item in new_data]
#             new_pin_indexes = [index for index, item in enumerate(en_data) if item.get('pin') in new_pins]
#
#             formatted_str_list.append('New Concert Information!')
#             for index in new_pin_indexes:
#                 concert = en_data[index]
#
#                 if concert['prc']:
#                     sorted_prices = sorted(concert['prc'], reverse=True)
#                     sorted_prices_str = ', '.join(map(str, sorted_prices))
#                 else:
#                     sorted_prices_str = '-'
#                 concert_date_str = ', '.join(concert['pdt'])
#
#                 if concert['sdt']:
#                     sale_date_str = ', '.join(concert['sdt'])
#                 else:
#                     sale_date_str = '-'
#
#                 if concert['loc']:
#                     location_str = ', '.join(concert['loc'])
#                 else:
#                     location_str = '-'
#
#                 formatted_str = f"""
# - {concert['tit']}
# - Ticket Date: {sale_date_str}
# - Date: {concert_date_str}
# - Price: {sorted_prices_str}
# - Location: {location_str}
# {concert['url']}
# """
#                 formatted_str_list.append(formatted_str.strip())
#
#         if check_if_today(plus_file):
#             formatted_str_list.append('Additional Concert Announced!')
#             plus_data = read_json(f"plus_concerts/{plus_file}")
#             plus_pins = [item['pin'] for item in plus_data]
#             plus_pin_indexes = [index for index, item in enumerate(en_data) if item.get('pin') in plus_pins]
#
#             for index in plus_pin_indexes:
#                 concert = en_data[index]
#
#                 if concert['prc']:
#                     sorted_prices = sorted(concert['prc'], reverse=True)
#                     sorted_prices_str = ', '.join(map(str, sorted_prices))
#                 else:
#                     sorted_prices_str = '-'
#                 concert_date_str = ', '.join(concert['pdt'])
#
#                 if concert['sdt']:
#                     sale_date_str = ', '.join(concert['sdt'])
#                 else:
#                     sale_date_str = '-'
#
#                 if concert['loc']:
#                     location_str = ', '.join(concert['loc'])
#                 else:
#                     location_str = '-'
#
#                 formatted_str = f"""
# - {concert['tit']}
# - Ticket Date: {sale_date_str}
# - Date: {concert_date_str}
# - Price: {sorted_prices_str}
# - Location: {location_str}
# {concert['url']}
# """
#                 formatted_str_list.append(formatted_str.strip())
#
#     return formatted_str_list

async def send_msg():
    chat_id = "1048509087"
    alarm_message = "要記得搶票喔!"
    await app.bot.send_message(chat_id=chat_id, text=alarm_message)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # app.add_handler(CommandHandler('start', start_command))
    # app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('custom', custom_command))
    # app.add_handler(CommandHandler('switch_language', switch_language_command))

    app.add_error_handler(error)

    scheduler = AsyncIOScheduler()
    # scheduler.add_job(send_daily_update, CronTrigger(hour=21))
    scheduler.add_job(send_msg, CronTrigger(hour=14, minute=22))
    scheduler.start()

    print('Go!')
    app.run_polling(poll_interval=3)
