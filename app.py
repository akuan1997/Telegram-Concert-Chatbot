from typing import Final  # 引入Final類型，用於定義常量
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot  # 從telegram模組引入Update類
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, \
    ContextTypes  # 從telegram.ext模組引入多個類和模組
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from fuzzywuzzy import fuzz
import yaml
import re
from datetime import datetime, timedelta

from get_keyword_indexes_en import *
from get_keyword_indexes_zh import *
from get_city_date_indexes import *
from read_json_function import *

TOKEN: Final = ''  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = ''  # 定義機器人的使用者名稱作為常量

# 创建调度器
scheduler = AsyncIOScheduler()

user_language_preferences = {}
user_status = {}
user_language_file = "user_preferred_language.txt"

""" zh config """
zh_model_path = r'models\nlu-20240704-160226-complex-bunker.tar.gz'  # zh model
zh_agent = Agent.load(zh_model_path)
zh_json = "concert_zh.json"

""" en config """
en_model_path = r'en_models\nlu-20240606-141412-glum-skirmish.tar.gz'
en_agent = Agent.load(en_model_path)
en_json = "concert_en.json"

time_units = {
    'second': 1,
    'seconds': 1,
    'sec': 1,
    'secs': 1,
    'minute': 60,
    'minutes': 60,
    'min': 60,
    'mins': 60,
    'hour': 3600,
    'hours': 3600,
    'day': 86400,
    'days': 86400,
    'week': 604800,
    'weeks': 604800,
    'month': 2592000,
    'months': 2592000,
}


def convert_time_to_seconds(sentence):
    # 使用正则表达式提取时间
    pattern = r'(\d+)\s*(seconds?|secs?|minutes?|mins?|hours?|days?|weeks?|months?)'
    matches = re.findall(pattern, sentence, re.IGNORECASE)

    total_seconds = 0
    for match in matches:
        value = int(match[0])
        unit = match[1].lower()
        total_seconds += value * time_units[unit]

    return total_seconds


def format_seconds(seconds):
    units = [
        ('year', 60 * 60 * 24 * 365),
        ('month', 60 * 60 * 24 * 30),
        ('week', 60 * 60 * 24 * 7),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1),
    ]

    result = []
    for name, count in units:
        value = seconds // count
        if value:
            seconds -= value * count
            unit_name = name if value == 1 else name + 's'
            result.append(f"{value} {unit_name}")

    return ', '.join(result) if result else "0 seconds"


time_units_zh = {
    '秒': 1,
    '秒鐘': 1,
    '分': 60,
    '分鐘': 60,
    '小時': 3600,
    '天': 86400,
    '周': 604800,
    '週': 604800,
    '月': 2592000,
}


def chinese_to_arabic(chinese_number):
    chinese_numerals = {
        '零': 0,
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 10,
    }

    num = 0
    if '十' in chinese_number:
        parts = chinese_number.split('十')
        if parts[0] == '':
            num += 10
        else:
            num += chinese_numerals[parts[0]] * 10
        if len(parts) > 1 and parts[1] != '':
            num += chinese_numerals[parts[1]]
    else:
        num = chinese_numerals[chinese_number]

    return num


def extract_chinese_number(chinese_time):
    pattern = r'(\d+|[\u4e00-\u9fff]+)\s*(秒鐘?|分鐘?|小時|天|周|週|月)'
    matches = re.findall(pattern, chinese_time)

    total_seconds = 0
    for match in matches:
        number, unit = match
        if number.isdigit():
            value = int(number)
        else:
            value = chinese_to_arabic(number)
        total_seconds += value * time_units_zh[unit]

    return total_seconds


def convert_time_to_seconds_zh(sentence):
    return extract_chinese_number(sentence)


def format_seconds_zh(seconds):
    units = [
        ('年', 60 * 60 * 24 * 365),
        ('月', 60 * 60 * 24 * 30),
        ('周', 60 * 60 * 24 * 7),
        ('天', 60 * 60 * 24),
        ('小時', 60 * 60),
        ('分鐘', 60),
        ('秒', 1),
    ]

    result = []
    for name, count in units:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{value} {name}")

    return ', '.join(result) if result else "0 秒"


def get_user_language(id):
    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if id in line:
            return line[line.index('|||') + 3:line.index('|||') + 5]


def show_concert_info(indexes, language):
    if not indexes:
        return [
            "對不起，我沒有找到相關的演唱會資訊。" if language == 'zh' else "Sorry, I couldn't find any relevant concert information."]

    formatted_str_list = []
    if language == 'zh':
        data = read_json("concert_zh.json")
    elif language == 'en':
        data = read_json("concert_en.json")

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

        if concert['loc']:
            location_str = ', '.join(concert['loc'])
        else:
            location_str = '-'

        if language == 'zh':
            formatted_str = f"""
- {concert['tit']}
- 售票日期: {sale_date_str}
- 表演日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 地點: {location_str}
{concert['url']}
            """
        elif language == 'en':
            formatted_str = f"""
- {concert['tit']}
- Sale Date: {sale_date_str}
- Date: {concert_date_str}
- Ticket Price: {sorted_prices_str}
- Location: {location_str}
{concert['url']}
            """

        formatted_str_list.append(formatted_str.strip())

    return formatted_str_list


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
    print(result['entities'])
    print('zh', result)
    print(f'find singer?', find_singer)
    print(f"intent: {result['intent']['name']}")
    print(f"score: {result['intent']['confidence']}")
    # if result['intent']['confidence'] > 0.6:
    #     print('信心程度大於六成')
    # print('--')

    if len(result['entities']) == 0:
        print('No Entities')
    else:
        if result['intent']['name'] == "query_ticket_time":
            ticket_time_indexes, user_prompt = zh_get_ticket_time(user_input, json_filename)
            found_keyword = False
            keyword_indexes = []
            keywords = []

            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                    if result['entities'][i]['entity'] == 'keyword':
                        found_keyword = True
                        keyword_index = get_keyword_indexes_zh(result['entities'][i]['value'], json_filename)
                        print(f"keyword_index = {keyword_index}")
                        keyword_indexes.extend(keyword_index)
                        keywords.append(result['entities'][i]['value'])

            if found_keyword and ticket_time_indexes:
                print('取集合')
                print(f"ticket_time_indexes = {ticket_time_indexes}")
                print(f"keyword_indexes = {keyword_indexes}")
                intersection = [item for item in keyword_indexes if item in ticket_time_indexes]
                user_prompt = [f"\"{user_prompt}\"且關鍵字為\"{', '.join(keywords)}\"的售票時間"]
                print(f"intersection = {intersection}")
                return intersection, user_prompt
            elif not found_keyword and ticket_time_indexes:
                print('直接搜尋售票時間')
                print(f"ticket_time_indexes = {ticket_time_indexes}")
                user_prompt = [f"\"{user_prompt}\"的售票時間"]
                return ticket_time_indexes, user_prompt
            elif found_keyword and not ticket_time_indexes:
                print('直接搜尋keyword')
                print(f"keyword_indexes = {keyword_indexes}")
                user_prompt = [f"關鍵字為\"{', '.join(keywords)}\"的售票時間"]
                return keyword_indexes, user_prompt
            else:
                print('直接回傳找不到')
                user_prompt = ["抱歉，我找不到任何資訊"]
                return user_prompt


        elif result['intent']['name'] == "query_keyword":

            found_datetime_city = False

            found_keyword = False

            keyword_indexes = []

            keywords = []

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
                        keywords.append(result['entities'][i]['value'])

            if found_keyword and found_datetime_city:
                print('取集合')
                print(f"keyword_indexes = {keyword_indexes}")
                dates_cities_indexes, user_dates_cities = zh_dates_cities(user_input, json_filename)
                print(f"dates_cities_indexes = {dates_cities_indexes}")
                intersection = [item for item in keyword_indexes if item in dates_cities_indexes]
                print(f"intersection = {intersection}")
                user_prompt = 'a2'
                print(f"user_dates_cities = {user_dates_cities}")
                user_prompt = [f"\"關鍵字: {', '.join(keywords)}\""]
                user_prompt.extend(user_dates_cities)
                print(f"user_prompt = {user_prompt}")
                return intersection, user_prompt
            elif not found_keyword and found_datetime_city:
                print('只搜尋日期')
                dates_cities_indexes, user_dates_cities = zh_dates_cities(user_input, json_filename)
                print(f"dates_cities_indexes = {dates_cities_indexes}")
                print(f"user_dates_cities = {user_dates_cities}")
                user_prompt = user_dates_cities
                print(f"user_prompt = {user_prompt}")
                return dates_cities_indexes, user_prompt
            elif found_keyword and not found_datetime_city:
                print('只搜尋關鍵字')
                print(f"keyword_indexes = {keyword_indexes}")
                user_prompt = [f"\"關鍵字: {', '.join(keywords)}\""]
                print(f"user_prompt = {user_prompt}")
                return keyword_indexes, user_prompt
            else:
                print('找不到關鍵字，也找不到日期，那就直接搜尋keyword_indexes')
                keyword_index = get_keyword_indexes_zh(user_input, json_filename)
                print(f"keyword_index = {keyword_index}")
                user_prompt = ["不好意思，我找不到任何的關鍵字、日期以及城市。我將會透過您的句子直接搜尋相關的資訊。"]
                print(f"user_prompt = {user_prompt}")
                return keyword_index, user_prompt


async def get_en_indexes(user_input, json_filename):
    with open('en_data/keyword.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    names = [name.replace(' ', '') for name in names]

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    message = user_input.lower()
    # print(f'ori msg: {message}')

    result = await en_agent.parse_message(message)
    print(result['entities'])

    print(f"intent: {result['intent']['name']}")
    print(f"score: {result['intent']['confidence']}")
    # if result['intent']['confidence'] > 0.6:
    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('--')
    if len(result['entities']) == 0:
        print('No Entities')
    else:
        if result['intent']['name'] == "query_ticket_time":
            ticket_time_indexes, user_prompt = en_get_ticket_time(user_input, json_filename)
            print(f"ticket_time_indexes = {ticket_time_indexes}")
            user_prompt = [f"Searching ticketing time \"{user_prompt}\" ..."]
            return ticket_time_indexes, user_prompt, 'ticketing time'

        elif result['intent']['name'] == "query_keyword":
            keywords = []
            found_datetime_city = False

            # print('test a')

            for i in range(len(result['entities'])):
                # print('test b')
                # if result['entities'][i]['value']:
                #     print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                # print(result['entities'][i]['value'])

                if result['entities'][i]['entity'] == 'datetime' or result['entities'][i]['entity'] == 'city':
                    found_datetime_city = True
                elif result['entities'][i]['entity'] == 'keyword':
                    keywords.append(result['entities'][i]['value'])

            if keywords:
                print(keywords)
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

                print(f"keyword = \"{keyword}\"")

                if found_datetime_city:
                    print('有keyword，也有datetime，取集合')
                    en_dates_cities_indexes, user_dates_cities, matched_tags = en_dates_cities(user_input,
                                                                                               json_filename)
                    matched_tags.append("keyword")
                    print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
                    print(f"user_dates_cities = {user_dates_cities}")
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(keyword, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    intersection = [item for item in get_keyword_indexes_en_indexes if item in en_dates_cities_indexes]
                    print(f"intersection = {intersection}")

                    # user_prompt = f"No problem! Searching \"keyword: {keyword}\", {user_dates_cities}"
                    user_prompt = [f"\"keyword: {keyword}\""]
                    user_prompt.extend(user_dates_cities)
                    print(f"user_prompt = {user_prompt}")
                    return intersection, user_prompt, matched_tags
                else:
                    print('有keyword，但是沒有datetime，直接顯示keyword indexes')
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(keyword, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    matched_tags = ["keyword"]

                    # user_prompt = f"No problem! Searching \"keyword: {keyword}\""
                    user_prompt = [f"\"keyword: {keyword}\""]
                    print(f"user_prompt = {user_prompt}")
                    return get_keyword_indexes_en_indexes, user_prompt, matched_tags
            else:
                print('沒有keyword')
                if found_datetime_city:
                    print(f"user_input = {user_input}")
                    en_dates_cities_indexes, user_dates_times, matched_tags = en_dates_cities(user_input, json_filename)
                    print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
                    print(f"user_dates_times = {user_dates_times}")

                    # user_prompt = f"No problem! Searching {user_dates_times}"
                    user_prompt = user_dates_times
                    print(f"user_prompt = {user_prompt}")
                    return en_dates_cities_indexes, user_prompt, matched_tags
                else:
                    print('沒有keyword，也沒有日期，直接把user_input拿去keyword搜尋')
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(user_input, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    matched_tags = []

                    user_prompt = f"Sorry, we couldn't find any keyword, date or city. We will search relevant information for you."
                    print(f"user_prompt = {user_prompt}")
                    return get_keyword_indexes_en_indexes, user_prompt, matched_tags


# 定義三個處理不同指令的異步函式
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     txt = f"""
    # 歡迎！ 請選擇你偏好的語言。
    # 輸入1 (中文)
    # 輸入2 (英文)
    # 語言可以隨時在左下角的menu當中選擇切換。
    # 如果沒有輸入我們將使用預設語言: 中文
    #
    # Welcome! Please choose your preferred language.
    # Enter 1 (Chinese)
    # Enter 2 (English)
    # You can always switch languages in the menu at the bottom left.
    # If no input is provided, we will use the default language: Chinese.
    # """
    # 添加選項
    keyboard = [
        [InlineKeyboardButton("English🇺🇸", callback_data='start_english')],
        [InlineKeyboardButton("繁體中文🇹🇼", callback_data='start_chinese')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    txt1 = f"""
歡迎！ 請選擇你偏好的語言。
語言可以隨時在左下角的menu當中選擇切換。

Welcome! Please choose your preferred language.
You can always switch languages in the menu at the bottom left.
"""
    # await update.message.reply_text(txt)
    await update.message.reply_text(txt1, reply_markup=reply_markup)


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Execute help command')


# # async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user_id = update.message.chat.id
# #     user_status[user_id] = ""
# #     print(user_status)
# #
# #     await update.message.reply_text(str(user_id))
# #     await update.message.reply_text('Execute custom aaa command')
#
#
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

    context.user_data['queries'] = []
    context.user_data['awaiting_new_query'] = False
    print('reset queries')


async def send_msg(chat_id, message):
    await app.bot.send_message(chat_id=chat_id, text=message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    message = update.message  # to detect reply
    user_input: str = update.message.text  # user input
    user_id = update.message.chat.id
    print(f'User ({user_id}): "{user_input}"')

    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.replace('\n', '').split('|||')[0] for line in lines]
    # print('handle message', lines)

    # 初始化查询列表，如果不存在的话
    if 'queries' not in context.user_data:
        context.user_data['queries'] = []

    if str(user_id) in lines:
        if get_user_language(str(user_id)) == 'zh':
            # chi, reply
            if message.reply_to_message:
                reply_message = message.reply_to_message
                reply_text = reply_message.text
                title = reply_text.split("\n")[0].replace('- ', '')
                print(f"title = {title}")
                sale_date_time = reply_text.split("\n")[1].split('- 售票日期: ')[1]
                print(f"sale_date_time = {sale_date_time}")
                if ',' in sale_date_time:
                    # 分割日期时间字符串并去除前后空格
                    date_times = [dt.strip() for dt in sale_date_time.split(',')]
                    print(f"date_times = {date_times}")
                    # 初始化 keyboard 列表
                    keyboard = []
                    # 创建按钮并添加到键盘列表
                    for i, dt in enumerate(date_times):
                        context.user_data[f'alarm_{i}_title'] = title
                        context.user_data[f'alarm_{i}_user_input'] = user_input
                        keyboard.append([InlineKeyboardButton(dt, callback_data=f'alarm_{i}')])
                    print(f"keyboard = {keyboard}")
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    print(f"reply_markup = {reply_markup}")
                    await update.message.reply_text(f'您想要為哪個時間設置鬧鐘呢?',
                                                    reply_markup=reply_markup)

                    return
                if ":" in sale_date_time:
                    # print(f"original user input = {user_input}")
                    # print(f"with function = {chinese_to_arabic(user_input)}")
                    user_input = user_input.replace('半小時', '30分鐘')
                    total_seconds = convert_time_to_seconds_zh(user_input)
                    reply_text_sale_date_time = datetime.strptime(sale_date_time, "%Y/%m/%d %H:%M")
                    alarm_date_time = reply_text_sale_date_time - timedelta(seconds=total_seconds)
                    print(f"alarm_date_time = {alarm_date_time}")
                    alarm_msg = f"售票提醒! {title} 將會在 {format_seconds_zh(total_seconds)} 後開始售票!"
                    print(f"alarm_msg = {alarm_msg}")

                    with open('ticket_alarm.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{user_id}|{alarm_date_time}|{alarm_msg}\n")

                    # scheduler.add_job(send_msg, CronTrigger(year=alarm_date_time.year,
                    #                                         month=alarm_date_time.month,
                    #                                         day=alarm_date_time.day,
                    #                                         hour=alarm_date_time.hour,
                    #                                         minute=alarm_date_time.minute,
                    #                                         second=alarm_date_time.second),
                    #                   args=[user_id, alarm_msg])
                    await reload_ticket_alarms()
                    await update.message.reply_text(
                        f"沒問題！ 我將會在 {alarm_date_time} 提醒您售票時間即將在 {format_seconds_zh(total_seconds)} 後開始！")
                else:
                    await update.message.reply_text("不好意思，你回覆的這則訊息沒有售票時間 :(")
                # await context.bot.send_message(chat_id=update.effective_chat.id,
                #                                text=f"你回覆的訊息是:\n{reply_text}\n輸入文字:\n{user_input}")  # test
                # now = datetime.now()
                # new_date_time = now + timedelta(seconds=5)
                # scheduler.add_job(send_msg, CronTrigger(hour=new_date_time.hour, minute=new_date_time.minute,
                #                                         second=new_date_time.second), args=[user_id, "你好呀"])
            # chi, direct msg
            else:
                # 检查是否在等待新查询
                if context.user_data.get('awaiting_new_query'):
                    await handle_new_search(update, context, user_input, 'zh')
                else:
                    # 存儲用戶輸入
                    context.user_data['queries'].append(user_input)

                    found_indexes, user_prompt = await get_zh_indexes(user_input, zh_json)

                    # <= 30 results
                    if len(found_indexes) <= 30:
                        context.user_data['queries'] = []
                        context.user_data['awaiting_new_query'] = False

                        messages = show_concert_info(found_indexes, 'zh')

                        await update.message.reply_text(f"正在查詢 {' & '.join(user_prompt)}")

                        print(f"一共找到{len(found_indexes)}筆資料")
                        await update.message.reply_text(f"一共找到 {len(found_indexes)} 筆資料")

                        for msg in messages:
                            await update.message.reply_text(msg)
                    # > 30 results
                    else:
                        # 添加選項
                        keyboard = [
                            [InlineKeyboardButton("顯示全部", callback_data='show_all')],
                            [InlineKeyboardButton("繼續搜尋", callback_data='continue_searching')],
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        print(f"reply_markup = {reply_markup}")
                        # await update.message.reply_text('請選擇下一步操作：', reply_markup=reply_markup)
                        await update.message.reply_text(
                            f'找到 {len(found_indexes)} 筆資料，您想要顯示全部還是繼續新增像是曲風、日期、城市 ... 等等的關鍵字呢?',
                            reply_markup=reply_markup)
        # eng
        else:
            # eng, reply
            if message.reply_to_message:
                reply_message = message.reply_to_message
                reply_text = reply_message.text
                title = reply_text.split("\n")[0].replace('- ', '')
                print(f"title = {title}")
                # sale_date_time = reply_text.split("\n")[1].replace('\n', '')
                sale_date_time = reply_text.split("\n")[1].split('- Sale Date: ')[1]
                print(f"sale_date_time = {sale_date_time}")
                if ',' in sale_date_time:
                    # 分割日期时间字符串并去除前后空格
                    date_times = [dt.strip() for dt in sale_date_time.split(',')]
                    print(f"date_times = {date_times}")
                    # 初始化 keyboard 列表
                    keyboard = []
                    # 创建按钮并添加到键盘列表
                    for i, dt in enumerate(date_times):
                        context.user_data[f'alarm_{i}_title'] = title
                        context.user_data[f'alarm_{i}_user_input'] = user_input
                        keyboard.append([InlineKeyboardButton(dt, callback_data=f'alarm_{i}')])
                    print(f"keyboard = {keyboard}")
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    print(f"reply_markup = {reply_markup}")
                    await update.message.reply_text(f'What Time Do You Want to Set the Alarm?',
                                                    reply_markup=reply_markup)

                    return

                if ":" in sale_date_time:
                    total_seconds = convert_time_to_seconds(user_input)
                    reply_text_sale_date_time = datetime.strptime(sale_date_time, "%Y/%m/%d %H:%M")
                    alarm_date_time = reply_text_sale_date_time - timedelta(seconds=total_seconds)
                    print(f"alarm_date_time = {alarm_date_time}")
                    alarm_msg = f"{title} is going to start selling after {format_seconds(total_seconds)}!"
                    print(f"alarm_msg = {alarm_msg}")

                    with open('ticket_alarm.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{user_id}|{alarm_date_time}|{alarm_msg}\n")

                    # scheduler.add_job(send_msg, CronTrigger(year=alarm_date_time.year,
                    #                                         month=alarm_date_time.month,
                    #                                         day=alarm_date_time.day,
                    #                                         hour=alarm_date_time.hour,
                    #                                         minute=alarm_date_time.minute,
                    #                                         second=alarm_date_time.second),
                    #                   args=[user_id, alarm_msg])
                    await reload_ticket_alarms()
                    await update.message.reply_text(
                        f"No problem! I will send a reminder message at {alarm_date_time} that the concert tickets will go on sale after {format_seconds(total_seconds)}!")
                    # await update.message.reply_text(
                    #     f"No problem! we will send you a message at {alarm_date_time} {format_seconds(total_seconds)} before tickets start selling!")
                else:
                    await update.message.reply_text("Sorry, this message does not contain selling time :(")
                # await context.bot.send_message(chat_id=update.effective_chat.id,
                #                                text=f"Replied to:\n{reply_text}\nYour input:\n{user_input}")  # test
                # now = datetime.now()
                # new_date_time = now + timedelta(seconds=5)
                # scheduler.add_job(send_msg, CronTrigger(hour=new_date_time.hour, minute=new_date_time.minute,
                #                                         second=new_date_time.second), args=[user_id, "你好呀"])
            # eng, direct msg
            else:
                # 检查是否在等待新查询
                if context.user_data.get('awaiting_new_query'):
                    await handle_new_search(update, context, user_input, 'en')
                else:
                    # 存儲用戶輸入
                    context.user_data['queries'].append(user_input)

                    found_indexes, user_prompt, matched_tags = await get_en_indexes(user_input, en_json)

                    # <= 30 results
                    if len(found_indexes) <= 30:
                        context.user_data['queries'] = []
                        context.user_data['awaiting_new_query'] = False

                        messages = show_concert_info(found_indexes, 'en')

                        print(f"matched_tags = {matched_tags}")

                        await update.message.reply_text(f"Searching {' & '.join(user_prompt)} ...")

                        print(f"一共找到{len(found_indexes)}筆資料")
                        await update.message.reply_text(f"We found {len(found_indexes)} results!")

                        for msg in messages:
                            await update.message.reply_text(msg)
                    # > 30 results
                    else:
                        # 添加選項
                        keyboard = [
                            [InlineKeyboardButton("Show All", callback_data='show_all')],
                            [InlineKeyboardButton("Continue Searching", callback_data='continue_searching')],
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        print(f"reply_markup = {reply_markup}")
                        # await update.message.reply_text('請選擇下一步操作：', reply_markup=reply_markup)
                        await update.message.reply_text(
                            f'We found {len(found_indexes)} results, would you like to show all the results or add more keyword like genre, date or city?',
                            reply_markup=reply_markup)

    #     elif user_input.strip() in ('1', '2'):
    #         user_language_preferences[user_id] = 'Chinese' if user_input.strip() == '1' else 'English'
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
    else:
        await update.message.reply_text("請先幫我設定您偏好的語言。\nPlease help me set your preferred language first.")

    # 重置计时器
    reset_timeout(update, context)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.message.chat.id

    await query.answer()
    choice = query.data
    print(f'choice = {choice}')

    # en
    if get_user_language(str(user_id)) == 'en':
        if choice == 'show_all':
            queries = context.user_data.get('queries', [])
            await query.edit_message_text(text="Show All Results.")
            await show_all_results(update, context, queries, 'en')
            # 繼續之前的查詢邏輯
        elif choice == 'continue_searching':
            await query.edit_message_text(
                text="No problem! Please tell me what keyword, date or city you would like to search.\n"
                     "Remember, the search mode will be terminated after 30 minutes of inactivity or when you click 'show all':")
            # 等待用戶新的輸入
            context.user_data['awaiting_new_query'] = True
        elif choice == 'start_english':
            await query.edit_message_text(text="You already set your preferred language to English.")
        elif choice == 'start_chinese':
            await query.edit_message_text(text="沒問題! 你的偏好語言已設定為中文!")
        elif choice.startswith('alarm_'):
            # 获取所有按钮
            buttons = query.message.reply_markup.inline_keyboard

            # 找到按下的按钮的文本
            button_text = None
            for button_row in buttons:
                for button in button_row:
                    if button.callback_data == choice:
                        button_text = button.text
                        break
            print(f"button_text = {button_text}")

            """"""

            index = choice.split('_')[1]
            title = context.user_data.get(f'alarm_{index}_title', 'Unknown Title')
            user_input = context.user_data.get(f'alarm_{index}_user_input', 'Unknown User Input')
            total_seconds = convert_time_to_seconds(user_input)
            reply_text_sale_date_time = datetime.strptime(button_text, "%Y/%m/%d %H:%M")
            alarm_date_time = reply_text_sale_date_time - timedelta(seconds=total_seconds)
            print(f"alarm_date_time = {alarm_date_time}")
            alarm_msg = f"{title} is going to start selling after {format_seconds(total_seconds)}!"
            print(f"alarm_msg = {alarm_msg}")

            with open('ticket_alarm.txt', 'a', encoding='utf-8') as f:
                f.write(f"{user_id}|{alarm_date_time}|{alarm_msg}\n")
            await reload_ticket_alarms()
            await query.edit_message_text(
                text=f"No problem! I will send a reminder message at {alarm_date_time} that the concert tickets will go on sale after {format_seconds(total_seconds)}!")
    # zh
    elif get_user_language(str(user_id)) == 'zh':
        if choice == 'show_all':
            queries = context.user_data.get('queries', [])
            await query.edit_message_text(text="顯示全部結果")
            await show_all_results(update, context, queries, 'zh')
            # 繼續之前的查詢邏輯
        elif choice == 'continue_searching':
            await query.edit_message_text(
                text="沒問題! 請輸入你想要查詢的關鍵字、日期或是城市\n"
                     "請記得，閒置30分鐘或是按下顯示全部後將會重置目前的搜尋。")
            # 等待用戶新的輸入
            context.user_data['awaiting_new_query'] = True
        elif choice == 'start_english':
            await query.edit_message_text(text="No problem! Your preferred language has been set to English!")
        elif choice == 'start_chinese':
            await query.edit_message_text(text="你已經將偏好語言設置為中文!")
        elif choice.startswith('alarm_'):
            # 获取所有按钮
            buttons = query.message.reply_markup.inline_keyboard

            # 找到按下的按钮的文本
            button_text = None
            for button_row in buttons:
                for button in button_row:
                    if button.callback_data == choice:
                        button_text = button.text
                        break
            print(f"button_text = {button_text}")

            """"""

            index = choice.split('_')[1]
            title = context.user_data.get(f'alarm_{index}_title', 'Unknown Title')
            user_input = context.user_data.get(f'alarm_{index}_user_input', 'Unknown User Input')
            user_input = user_input.replace('半小時', '30分鐘')
            total_seconds = convert_time_to_seconds_zh(user_input)
            reply_text_sale_date_time = datetime.strptime(button_text, "%Y/%m/%d %H:%M")
            alarm_date_time = reply_text_sale_date_time - timedelta(seconds=total_seconds)
            print(f"alarm_date_time = {alarm_date_time}")
            alarm_msg = f"售票提醒! {title} 將會在 {format_seconds_zh(total_seconds)} 後開始售票!"
            print(f"alarm_msg = {alarm_msg}")

            with open('ticket_alarm.txt', 'a', encoding='utf-8') as f:
                f.write(f"{user_id}|{alarm_date_time}|{alarm_msg}\n")

            await reload_ticket_alarms()
            await query.edit_message_text(
                f"沒問題！ 我將會在 {alarm_date_time} 提醒您售票時間即將在 {format_seconds_zh(total_seconds)} 後開始！")
    else:
        if choice == 'start_english':
            txt = """
No problem! Your preferred language has been set to English!

---

Usage Instructions:

1. You can search for upcoming concerts by artist name, music genre, city, or specific date.
   Example: "Jay Chou", "rap", "Taipei", "tomorrow"

2. You can also search using multiple criteria in one sentence.
   Example: "Taylor Swift Taipei", "Post Malone next month", "hip-hop this week Tainan"

3. You can search using any keyword and then add more keywords based on the number of search results. We will continue to search for results that match the conditions and present them to you based on the existing keywords.

4. Additionally, you can search for concerts that will start selling tickets soon.
   Example: "Find concerts starting ticket sales tomorrow", "ticket sales time, today and tomorrow"

5. You can reply to concert information with a specific time, and the chatbot will remind you to pay attention to the ticket sale time before it starts.

6. Every night at 9 PM, I will send you today's announcements and additional concert information!

7. If the chat room is idle for 30 minutes, it will reset your current search. However, the chatbot will not send a message specifically to remind you that the search has been reset.

Have Fun!
            """
            await query.edit_message_text(text=txt)
            with open(user_language_file, 'a', encoding='utf-8') as f:
                f.write(f"{user_id}|||en\n")
        elif choice == 'start_chinese':
            txt = """
沒問題! 你的偏好語言已設定為中文! 以下是聊天機器人使用的教學，幫助您更快地了解如何使用。

---

1. 你可以通過搜尋歌手名稱、音樂類型、城市或特定時間來查詢即將舉行的音樂會。
範例："周杰倫", "饒舌", "台北", "明天"

2. 你也可以在一個句子當中同時搜尋多個條件。
範例："蔡依林 台北", "Post Malone 下個月", "嘻哈 這周 台南"

3. 您也可以先搜巡任意的關鍵字並根據搜尋結果的數量新增關鍵字，我們將會在現有的關鍵字繼續搜尋符合條件的結果並呈現給您。

4. 此外，你還可以搜尋即將開始售票的音樂會。範例："查找明天開始售票的音樂會", "售票時間，今天和明天"

5. 您可以回覆演唱會訊息並輸入時間，聊天機器人將會在售票時間前提醒您要記得注意搶票時間。

6. 每天晚上九點，我將會傳送今日宣布以及加場的演唱會資訊給您!

7. 如果聊天室閒置30分鐘，聊天室將會重置您目前的搜尋。但是聊天機器人並不會特別發出消息提醒您目前的搜尋已經重置。

祝您演唱會玩得開心！
            """
            await query.edit_message_text(text=txt)
            with open(user_language_file, 'a', encoding='utf-8') as f:
                f.write(f"{user_id}|||zh\n")


async def show_all_results(update: Update, context: ContextTypes.DEFAULT_TYPE, queries, language):
    # 获取回调查询的消息对象
    message = update.callback_query.message

    # 重置查询列表
    print(f"queries = {queries}")

    if language == 'en':
        # found_indexes, user_prompt, matched_tags = await get_en_indexes(user_input, en_json)
        if len(queries) == 1:
            found_indexes, user_prompt, matched_tags = await get_en_indexes(queries[0], en_json)

            messages = show_concert_info(found_indexes, 'en')
            print(f"matched_tags = {matched_tags}")

            # await update.message.reply_text(user_prompt)
            await message.reply_text(f"Searching {' & '.join(user_prompt)}")

            print(f"一共找到{len(found_indexes)}筆資料")
            # await message.reply_text(f"We found {len(found_indexes)} results!")

            for msg in messages:
                await message.reply_text(msg)
        else:
            result_indexes, _, _ = await get_en_indexes(queries[0], en_json)
            for i in range(1, len(queries)):
                next_indexes, _, _ = await get_en_indexes(queries[i], en_json)
                result_indexes = set(result_indexes) & set(next_indexes)
            result_indexes = list(result_indexes)
            print(f"result_indexes = {result_indexes}")

            messages = show_concert_info(result_indexes, 'en')
            print(f"一共找到{len(result_indexes)}筆資料")
            # await message.reply_text(f"We found {len(result_indexes)} results!")

            for msg in messages:
                await message.reply_text(msg)
    else:
        # found_indexes, user_prompt, matched_tags = await get_en_indexes(user_input, en_json)
        if len(queries) == 1:
            found_indexes, user_prompt = await get_zh_indexes(queries[0], zh_json)

            messages = show_concert_info(found_indexes, 'zh')

            # await update.message.reply_text(user_prompt)
            await message.reply_text(f"Searching {' & '.join(user_prompt)}")

            print(f"一共找到{len(found_indexes)}筆資料")
            # await message.reply_text(f"We found {len(found_indexes)} results!")

            for msg in messages:
                await message.reply_text(msg)

            context.user_data['queries'] = []
            context.user_data['awaiting_new_query'] = False
            await update.callback_query.edit_message_text(text="Show All Results. Search has been reset.")
        else:
            result_indexes, _ = await get_zh_indexes(queries[0], zh_json)
            for i in range(1, len(queries)):
                next_indexes, _ = await get_zh_indexes(queries[i], zh_json)
                result_indexes = set(result_indexes) & set(next_indexes)
            result_indexes = list(result_indexes)
            print(f"result_indexes = {result_indexes}")

            messages = show_concert_info(result_indexes, 'zh')
            print(f"一共找到{len(result_indexes)}筆資料")
            # await message.reply_text(f"We found {len(result_indexes)} results!")

            for msg in messages:
                await message.reply_text(msg)

    context.user_data['queries'] = []
    context.user_data['awaiting_new_query'] = False
    await update.callback_query.edit_message_text(text="顯示全部結果，搜尋已重置。")


async def handle_new_search(update: Update, context: ContextTypes.DEFAULT_TYPE, new_query: str, language):
    context.user_data['queries'].append(new_query)
    await perform_search(update, context, language)


async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE, language):
    # 在這裡執行你的搜索邏輯，例如調用Rasa模型或查詢數據庫
    queries = context.user_data.get('queries', [])
    # print(f"queries = {queries}")
    # search_results = f"根據您的新關鍵字 '{query}' 和之前的查詢 {queries[:-1]} 進行搜索。"
    # await update.message.reply_text(search_results)

    # Check if the update is a callback query or a message
    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message

    if language == 'en':
        if len(queries) == 1:
            found_indexes, user_prompt, _ = await get_en_indexes(queries[0], en_json)
            print(f"一共找到{len(found_indexes)}筆資料")
            await message.reply_text(f"We found {len(found_indexes)} results by searching {' & '.join(user_prompt)}!")
        else:
            result_indexes, user_prompts, _ = await get_en_indexes(queries[0], en_json)
            for i in range(1, len(queries)):
                next_indexes, user_prompt, _ = await get_en_indexes(queries[i], en_json)
                user_prompts.extend(user_prompt)
                result_indexes = set(result_indexes) & set(next_indexes)
            result_indexes = list(result_indexes)
            print(f"result_indexes = {result_indexes}")

            await message.reply_text(f"We found {len(result_indexes)} results by searching {' & '.join(user_prompts)}!")

        # 添加選項
        keyboard = [
            [InlineKeyboardButton("Show All", callback_data='show_all')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        print(f"reply_markup = {reply_markup}")
        # queries_str = '\n'.join(queries)
        # await update.message.reply_text(f'Current queries:\n{queries_str}', reply_markup=reply_markup)
        await update.message.reply_text(f'You can add more keywords, or', reply_markup=reply_markup)
    else:
        if len(queries) == 1:
            found_indexes, user_prompt = await get_zh_indexes(queries[0], zh_json)
            print(f"一共找到{len(found_indexes)}筆資料")
            await message.reply_text(f"透過搜尋 {' & '.join(user_prompt)} 一共找到 {len(found_indexes)} 筆資料!")
        else:
            result_indexes, user_prompts = await get_zh_indexes(queries[0], zh_json)
            for i in range(1, len(queries)):
                next_indexes, user_prompt = await get_zh_indexes(queries[i], zh_json)
                user_prompts.extend(user_prompt)
                result_indexes = set(result_indexes) & set(next_indexes)
            result_indexes = list(result_indexes)
            print(f"result_indexes = {result_indexes}")

            await message.reply_text(f"透過搜尋 {' & '.join(user_prompts)} 一共找到 {len(result_indexes)} 筆資料!")

        # 添加選項
        keyboard = [
            [InlineKeyboardButton("顯示全部", callback_data='show_all')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        print(f"reply_markup = {reply_markup}")
        # queries_str = '\n'.join(queries)
        # await update.message.reply_text(f'Current queries:\n{queries_str}', reply_markup=reply_markup)
        await update.message.reply_text(f'你可以新增更多關鍵字，或是', reply_markup=reply_markup)

    """"""


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print(f'Update {update} caused error {context.error}')
        user_id = None

        if update:
            if update.message:
                user_id = update.message.chat.id
            elif update.callback_query:
                user_id = update.callback_query.message.chat.id

        if user_id:
            try:
                if get_user_language(str(user_id)) == 'zh':
                    await context.bot.send_message(chat_id=user_id, text="對不起，我不太理解。")
                else:
                    await context.bot.send_message(chat_id=user_id, text="Sorry, I don't understand.")
            except Exception as inner_exception:
                print(f"An error occurred while sending a message: {inner_exception}")
        else:
            print("User ID could not be determined from the update.")
    except Exception as e:
        print(f"An error occurred while handling the error: {e}")


async def send_daily_update():
    with open(user_language_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    zh_texts = ['中文1', '中文2']
    en_texts = ['eng1', 'eng2']
    for line in lines:
        user_id, language = line.strip().split('|||')
        user_id = int(user_id)
        if language == 'zh':
            msgs = await get_daily_msg('zh')
            for msg in msgs:
                await app.bot.send_message(chat_id=user_id, text=msg)
        else:
            msgs = await get_daily_msg('en')
            for msg in msgs:
                await app.bot.send_message(chat_id=user_id, text=msg)


def check_if_today(text):
    pattern = r"concert_(\d{1,2})_(\d{1,2})_(\d{1,2}).json"
    month_day = re.search(pattern, text)
    month = int(month_day.group(1))
    day = int(month_day.group(2))

    # print(month, datetime.now().month)
    # print(day, datetime.now().day)
    if month == datetime.now().month and day == datetime.now().day:
        return True
    else:
        return False


async def get_daily_msg(language):
    new_file = get_latest_json_filename("new_concerts")
    plus_file = get_latest_json_filename("plus_concerts")

    if not (check_if_today(new_file) or check_if_today(plus_file)):
        if language == 'zh':
            formatted_str_list = ["今天沒有任何的資訊"]
        else:
            formatted_str_list = ["The is no information today."]

        print('no new file and no plus file')
        return formatted_str_list

    # data = read_json(json_filename)
    # pins = [item['pin'] for item in data]
    #
    # pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in pins]

    formatted_str_list = []

    if language == 'zh':
        zh_data = read_json("concert_zh.json")

        if check_if_today(new_file):
            new_data = read_json(f"new_concerts/{new_file}")
            new_pins = [item['pin'] for item in new_data]
            new_pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in new_pins]

            formatted_str_list.append('新的演唱會資訊!')
            for index in new_pin_indexes:
                concert = zh_data[index]

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

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- 售票日期: {sale_date_str}
- 表演日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 地點: {location_str}
{concert['url']}
                                        """
                formatted_str_list.append(formatted_str.strip())

        if check_if_today(plus_file):
            plus_data = read_json(f"plus_concerts/{plus_file}")
            plus_pins = [item['pin'] for item in plus_data]
            plus_pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in plus_pins]

            formatted_str_list.append('新的加場資訊!')
            for index in plus_pin_indexes:
                concert = zh_data[index]

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

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- 售票日期: {sale_date_str}
- 表演日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 地點: {location_str}
{concert['url']}
                                                    """
                formatted_str_list.append(formatted_str.strip())

    if language == 'en':
        en_data = read_json("concert_en.json")

        if check_if_today(new_file):
            new_data = read_json(f"new_concerts/{new_file}")
            new_pins = [item['pin'] for item in new_data]
            new_pin_indexes = [index for index, item in enumerate(en_data) if item.get('pin') in new_pins]

            formatted_str_list.append('Here\'s the New Concert Information for Today!')
            for index in new_pin_indexes:
                concert = en_data[index]

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

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- Sale Date: {sale_date_str}
- Date: {concert_date_str}
- Price: {sorted_prices_str}
- Location: {location_str}
{concert['url']}
"""
                formatted_str_list.append(formatted_str.strip())

        if check_if_today(plus_file):
            formatted_str_list.append('Additional Concert Announced!')
            plus_data = read_json(f"plus_concerts/{plus_file}")
            plus_pins = [item['pin'] for item in plus_data]
            plus_pin_indexes = [index for index, item in enumerate(en_data) if item.get('pin') in plus_pins]

            for index in plus_pin_indexes:
                concert = en_data[index]

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

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- Sale Date: {sale_date_str}
- Date: {concert_date_str}
- Price: {sorted_prices_str}
- Location: {location_str}
{concert['url']}
"""
                formatted_str_list.append(formatted_str.strip())

    return formatted_str_list


def reset_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    job = context.user_data.get('timeout_job')
    if job:
        job.remove()

    job = scheduler.add_job(
        send_reset_message,
        trigger=IntervalTrigger(minutes=30),
        args=[update, context],
    )
    context.user_data['timeout_job'] = job


async def send_reset_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_new_query'] = False
    context.user_data['queries'] = []
    # await update.message.reply_text("Query status has been reset due to 30 minutes of inactivity.")
    job = context.user_data.pop('timeout_job', None)
    if job:
        job.remove()

async def reload_ticket_alarms():
    print("ticket_alarm.txt has been modified, reloading alarms...")
    # 读取并处理ticket_alarm.txt文件
    with open('ticket_alarm.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]
    for line in lines:
        user_id, alarm_date_time, alarm_msg = line.split('|')
        alarm_date_time = datetime.strptime(alarm_date_time, "%Y-%m-%d %H:%M:%S")

        # 删除旧的定时任务
        job = scheduler.get_job(user_id)
        if job:
            job.remove()

        # 添加新的定时任务
        scheduler.add_job(send_msg, CronTrigger(year=alarm_date_time.year,
                                                month=alarm_date_time.month,
                                                day=alarm_date_time.day,
                                                hour=alarm_date_time.hour,
                                                minute=alarm_date_time.minute,
                                                second=alarm_date_time.second),
                          args=[user_id, alarm_msg], id=user_id)
        # print(f"{alarm_date_time} 提醒 {user_id}: {alarm_msg}")

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('switch_language', switch_language_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    # scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_update, CronTrigger(hour=21))
    with open('ticket_alarm.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = [line for line in lines]
    for line in lines:
        if line == "":
            continue
        user_id, alarm_date_time, alarm_msg = line.split('|')[0], datetime.strptime(line.split('|')[1],
                                                                                    "%Y-%m-%d %H:%M:%S"), \
            line.split('|')[2]

        scheduler.add_job(send_msg, CronTrigger(year=alarm_date_time.year,
                                                month=alarm_date_time.month,
                                                day=alarm_date_time.day,
                                                hour=alarm_date_time.hour,
                                                minute=alarm_date_time.minute,
                                                second=alarm_date_time.second),
                          args=[user_id, alarm_msg])
        print(f"{alarm_date_time} 提醒 {user_id}: {alarm_msg}")

    scheduler.start()

    print('Go!')
    app.run_polling(poll_interval=3)
