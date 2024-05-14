# https://www.youtube.com/watch?v=vZtm1wuA2yc&t=1183s&ab_channel=Indently
from typing import Final  # 引入Final類型，用於定義常量

from telegram import Update  # 從telegram模組引入Update類
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # 從telegram.ext模組引入多個類和模組

import asyncio
import logging
from typing import Text

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from fuzzywuzzy import fuzz
import yaml
import re

from get_keyword_indexes_en import *
from get_keyword_indexes_zh import *
from get_city_date_indexes import *
from function_read_json import *

TOKEN: Final = '6732658127:AAHc75srUIqqplCdlisn-TeecqlYRyCPUFM'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@kuan_concert_chatbot_test1_bot'  # 定義機器人的使用者名稱作為常量

user_language_preferences = {}
user_status = {}
user_language_file = "user_preferred_language.txt"

""" zh config """
zh_model_path = r'models/nlu-20240501-165733-frayed-acre.tar.gz'  # zh model
zh_agent = Agent.load(zh_model_path)
zh_json = "concert_zh.json"

""" en config """
en_model_path = r'en_models/nlu-20240511-033142-brilliant-set.tar.gz'
en_agent = Agent.load(en_model_path)
en_json = "concert_en.json"


def get_user_language(id):
    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if id in line:
            return line[line.index('|||') + 3:line.index('|||') + 5]


def show_concert_info(indexes, language):
    if not indexes:
        return "對不起，我沒有找到相關的演唱會資訊。" if language == 'zh' else "Sorry, I couldn't find any relevant concert information."

    formatted_str_list = []
    if language == 'zh':
        data = read_json("concert_zh.json")
        print('zh', len(data))
    elif language == 'en':
        data = read_json("concert_en.json")
        print('en', len(data))

    for index in indexes:
        if index >= len(data):
            print(f"索引 {index} 超出範圍，最大索引值應該小於 {len(data)}")
            continue

        concert = data[index]
        if concert['prc']:
            sorted_prices = sorted(concert['prc'], reverse=True)
            sorted_prices_str = ', '.join(map(str, sorted_prices))
        else:
            sorted_prices_str = '-'
        concert_date_str = ', '.join(concert['pdt'])
        if concert['sdt']:
            sale_date_str = ', '.join(concert['sdt'])
        else:
            sale_date_str = '-'

        if language == 'zh':
            formatted_str = f"""
- {concert['tit']}
- 日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 售票日期: {sale_date_str}
- {concert['url']}
            """
            formatted_str_list.append(formatted_str)
        elif language == 'en':
            formatted_str = f"""
- {concert['tit']}
- Date: {concert_date_str}
- Ticket Price: {sorted_prices_str}
- Sale Date: {sale_date_str}
- {concert['url']}
            """
            formatted_str_list.append(formatted_str)

    final_str = "\n".join(formatted_str_list)
    print(final_str)

    return final_str


def keyword_adjustment_optimized(user_input):
    with open('data/keyword.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    names_set = {name.lower() for name in names}
    english_words = re.findall(r'[A-Za-z0-9]+', user_input.lower())
    print(f"english_words = {english_words}")

    for word in english_words:
        if word in names_set:
            return user_input, True

    for word in english_words:
        for name in names:
            if fuzz.partial_ratio(word, name.lower()) > 80:
                user_input = user_input.replace(word, name)
                return user_input, True

    return user_input, False


async def get_zh_indexes(user_input, json_filename):
    print(f"原本的輸入: {user_input}")
    user_input, find_singer = keyword_adjustment_optimized(user_input)
    print(f"經過方程式後的輸入: {user_input}")
    result = await zh_agent.parse_message(user_input)
    print('zh', result)
    print(f'find singer?', find_singer)
    print(f"intent: {result['intent']['name']}")
    print(f"score: {result['intent']['confidence']}")
    if result['intent']['confidence'] > 0.6:
        print('信心程度大於六成')
    print('--')

    if len(result['entities']) == 0:
        print('No Entities')
    else:
        if result['intent']['name'] == "query_ticket_time":
            ticket_time_indexes = zh_get_ticket_time(user_input, json_filename)
            found_keyword = False
            keyword_indexes = []

            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                    if result['entities'][i]['entity'] == 'keyword':
                        found_keyword = True
                        keyword_index = get_keyword_indexes_zh(result['entities'][i]['value'], json_filename)
                        print(f"keyword_index = {keyword_index}")
                        keyword_indexes.extend(keyword_index)

            if found_keyword and ticket_time_indexes:
                print('取集合')
                print(f"ticket_time_indexes = {ticket_time_indexes}")
                print(f"keyword_indexes = {keyword_indexes}")
                intersection = [item for item in keyword_indexes if item in ticket_time_indexes]
                print(f"intersection = {intersection}")
                return intersection
            elif not found_keyword and ticket_time_indexes:
                print('直接搜尋售票時間')
                print(f"ticket_time_indexes = {ticket_time_indexes}")
                return ticket_time_indexes
            elif found_keyword and not ticket_time_indexes:
                print('直接搜尋keyword')
                print(f"keyword_indexes = {keyword_indexes}")
                return keyword_indexes
            else:
                print('直接回傳找不到')
                return []

        elif result['intent']['name'] == "query_keyword":
            found_datetime_city = False
            found_keyword = False
            keyword_indexes = []
            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")

                    if result['entities'][i]['entity'] == 'datetime' or result['entities'][i]['entity'] == 'city':
                        found_datetime_city = True
                        print(f"found_datetime_city = {found_datetime_city}")

                    if result['entities'][i]['entity'] == 'keyword':
                        found_keyword = True
                        keyword_index = get_keyword_indexes_zh(result['entities'][i]['value'], json_filename)
                        print(f"keyword_index = {keyword_index}")
                        keyword_indexes.extend(keyword_index)

            if found_keyword and found_datetime_city:
                print('取集合')
                print(f"keyword_indexes = {keyword_indexes}")
                dates_cities_indexes = zh_dates_cities(user_input, json_filename)
                print(f"dates_cities_indexes = {dates_cities_indexes}")
                intersection = [item for item in keyword_indexes if item in dates_cities_indexes]
                print(f"intersection = {intersection}")
                return intersection
            elif not found_keyword and found_datetime_city:
                print('只搜尋日期')
                dates_cities_indexes = zh_dates_cities(user_input, json_filename)
                print(f"dates_cities_indexes = {dates_cities_indexes}")
                return dates_cities_indexes
            elif found_keyword and not found_datetime_city:
                print('只搜尋關鍵字')
                print(f"keyword_indexes = {keyword_indexes}")
                return keyword_indexes
            else:
                print('直接回傳找不到')
                return []


async def get_en_indexes(user_input, json_filename):
    with open('en_data/keyword.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    names = [name.replace(' ', '') for name in names]

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    message = user_input.lower()
    print(f'ori msg: {message}')

    result = await en_agent.parse_message(message)

    print(f"intent: {result['intent']['name']}")
    print(f"score: {result['intent']['confidence']}")
    if result['intent']['confidence'] > 0.6:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('--')
    if len(result['entities']) == 0:
        print('No Entities')
    else:
        if result['intent']['name'] == "query_ticket_time":
            ticket_time_indexes = en_get_ticket_time(user_input, json_filename)
            print(f"ticket_time_indexes = {ticket_time_indexes}")
            return ticket_time_indexes
        elif result['intent']['name'] == "query_keyword":
            keywords = []
            found_datetime = False

            for i in range(len(result['entities'])):
                if result['entities'][i]['entity'] == 'datetime':
                    found_datetime = True
                elif result['entities'][i]['entity'] == 'keyword':
                    keywords.append(result['entities'][i]['value'])

            if keywords:
                keyword = max(keywords, key=len)

                found_keyword = False
                for j, name in enumerate(names):
                    if name.lower() == keyword.lower():
                        keyword = names[j]
                        found_keyword = True
                        break

                if not found_keyword:
                    print('沒有在keyword.yml當中找到keyword')
                    keyword = keyword.title()
                else:
                    print('有在keyword.yml當中找到keyword')

                print(f"keyword = {keyword}")
                if found_datetime:
                    print('有keyword，也有datetime，取集合')
                    en_dates_cities_indexes = en_dates_cities(user_input, json_filename)
                    print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(keyword, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    intersection = [item for item in get_keyword_indexes_en_indexes if item in en_dates_cities_indexes]
                    print(f"intersection = {intersection}")
                    return intersection
                else:
                    print('有keyword，但是沒有datetime，直接顯示keyword indexes')
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(keyword, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    return get_keyword_indexes_en_indexes
            else:
                print('沒有keyword')
                if found_datetime:
                    en_dates_cities_indexes = en_dates_cities(user_input, json_filename)
                    print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
                    return en_dates_cities_indexes
                else:
                    print('什麼都沒有')
                    return []


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
            found_indexes = await get_zh_indexes(text, zh_json)
            show_str = show_concert_info(found_indexes, 'zh')
            await update.message.reply_text(show_str)
        else:
            found_indexes = await get_en_indexes(text, en_json)
            show_str = show_concert_info(found_indexes, 'en')
            await update.message.reply_text(show_str)
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


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('switch_language', switch_language_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Go!')
    app.run_polling(poll_interval=3)
