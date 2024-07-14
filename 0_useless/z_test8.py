import asyncio
import logging
from typing import Text

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from fuzzywuzzy import fuzz
import yaml
import re


def load_keywords(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    examples_text = data['nlu'][0]['examples']
    keywords = [line.replace('- ', '').strip() for line in examples_text.split('\n') if line.strip() != '']
    return keywords


def find_best_match(input_text, keywords):
    input_text = input_text.lower()
    best_match = None
    highest_score = 0

    # 使用 token_sort_ratio 來改善多詞匹配
    for keyword in keywords:
        score = fuzz.token_sort_ratio(input_text, keyword.lower())
        if score > highest_score:
            highest_score = score
            best_match = keyword

    return best_match, highest_score


def run_cmdline(model_path: Text, words) -> None:
    """Loops over CLI input, passing each message to a loaded NLU model."""
    agent = Agent.load(model_path)

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    for word in words:
        message = word
        print('User input:', message)

        result = asyncio.run(agent.parse_message(message))

        print(f"intent: {result['intent']['name']}")
        print(f"score: {result['intent']['confidence']}")
        if result['intent']['confidence'] > 0.6:
            if result['intent']['name'] == 'query_keyword':
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                best_match, score = find_best_match(message, keywords)
                print(f"User input: {message}")
                print(f"Did you mean: {best_match} (score: {score})\n")
        if len(result['entities']) == 0:
            with open('../data/keyword.yml', 'r', encoding='utf-8') as f:
                singers = yaml.safe_load(f)
            singers = [singer.lower() for singer in singers]
            if message.lower() in singers:
                print('model找不到歌手，但是透過比對找到')
                print(message)
            """
            鄭伊健 (Ekin Cheng) 名字必須分開
            """
            print('No Entities')
        else:
            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")

        print('-----------------------------------------------')


logger = logging.getLogger(__name__)
keywords = load_keywords('../data/keyword.yml')
cities = load_keywords('../data/city.yml')

words1 = [
    'Post Malone',
    'Post Malone 演唱會',
    '演唱會 post malone',
    'ive 演唱會',
    '演唱會 IVE',
    'newjeans',
    'NewJeans 演唱會',
    '演唱會 NewJeans',
    'Le Sserafim',
    'LE SSERAFIM 演唱會',
    '台北 演唱會',
    '桃園 下周',
    '下個月 新北',
    '請告訴我有關IVE演唱會的資訊',
    '爵士音樂',
    '爵士樂',
    '請問這位歌手的演唱會將在哪個城市舉行？',
    'IVE',
    'stayc',
    'aespa',
    'wheein',
    '如果我想知道這個週末在台北以外的城市有哪些饒舌演唱會，該怎麼查詢？',
    '明天在台北的饒舌演唱會之外，後天在其他城市有類似活動嗎？',
    'ziont',
    '那麼後天呢？在台北或其他城市有類似的饒舌演唱會嗎？',
    '鄧福如',
    'postmalone',
    'taylorswift',
    '你好呀 ive',
    '我真的蠻喜歡postmalone的',
    '我真的蠻喜歡post malone的',
    '我真的蠻喜歡Post Malone的',
    '鄭伊健',
    'new jeans最近會來開演唱會嗎',
    'newjeans最近會來開演唱會嗎',
    'Apink CHOBOM的演唱會資訊',
    '請告訴我iu的演唱會資訊',
    "請告訴我有關於李泳知的演唱會消息",
    '請告訴我'
]
words2 = [
    '那麼下周呢',
    '那台北呢',
    '那下個月呢',
    '如果是後天呢',
]
words3 = [
    '鄭伊健',
    '請告訴我鄭伊健的演唱會資訊',
    '請告訴我IU的演唱會資訊',
    "陳奕迅那首歌 是唱他他自己 男人歌",
    "你可以告訴我鄭伊健的演唱會資訊嗎"
]
# model_path = r'models\nlu-20240216-234555-uniform-calico.tar.gz'
model_path = r'../models/nlu-20240501-165733-frayed-acre.tar.gz'

# run_cmdline(model_path, words1)
# run_cmdline(model_path, words2)
# run_cmdline(model_path, words3)
run_cmdline(model_path, words1)
