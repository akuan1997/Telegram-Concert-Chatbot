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

""" zh config """
zh_model_path = r'../models/nlu-20240501-165733-frayed-acre.tar.gz'  # zh model
zh_agent = Agent.load(zh_model_path)
zh_json = "concert_zh.json"

TOKEN: Final = '7219739601:AAEYdGgpr4DOxH6YrIKbtm7eCQeXoOCqyTY'  # 定義Telegram Bot的token作為常量
BOT_USERNAME: Final = '@Concert_info_chat_bot'  # 定義機器人的使用者名稱作為常量


def keyword_adjustment_optimized(user_input):
    with open('../data/keyword.yml', 'r', encoding='utf-8') as f:
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
            print(f'user_prompt = {user_prompt}')
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
                        keywords.append(result['entities'][i]['value'])
                        found_keyword = True
                        keyword_index = get_keyword_indexes_zh(result['entities'][i]['value'], json_filename)
                        print(f"keyword_index = {keyword_index}")
                        keyword_indexes.extend(keyword_index)

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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input: str = update.message.text  # user input
    _, user_prompt = await get_zh_indexes(user_input, "../concert_zh.json")
    print(user_prompt)
    await update.message.reply_text(f"正在為您搜尋 {' & '.join(user_prompt)}")
    # print(f"user_input = {user_input}")
    # await update.message.reply_text(
    #     f"沒問題！ 我將會在售票時間前 {format_seconds_zh(total_seconds)} 傳送一個訊息提醒您記得注意售票時間！")


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print('Go!')
    app.run_polling(poll_interval=3)
