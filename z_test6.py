import asyncio
import logging
from typing import Text

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from fuzzywuzzy import fuzz
import yaml
import re


def keyword_adjustment(user_input):
    # print(user_input)
    with open('data/keyword.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    names_without_space = [name.replace(' ', '') for name in names]

    # 匹配英文单词
    english_words = re.findall(r'[A-Za-z0-9]+', user_input)
    # 将匹配到的英文单词拼接起来
    english_part = ' '.join(english_words)

    ''''''

    # Post Malone
    # print('round 1')
    for name in names:
        if name in english_part:
            return user_input, True

    ''''''

    # post malone
    # print('round 2')
    for name in names:
        if name.lower() in user_input.lower():
            start_index = user_input.lower().find(name.lower())
            end_index = start_index + len(name.lower()) - 1
            user_input = user_input.replace(user_input[start_index:end_index + 1], name)
            return user_input, True

    ''''''

    english_split = english_part.split(' ')

    for i, name in enumerate(names_without_space):
        for e_split in english_split:
            score = fuzz.partial_ratio(e_split.lower(), name.lower())
            if score >= 80:
                # print('abc', score)
                # print(e_split.lower(), name.lower())
                if len(name) - 1 < len(e_split) < len(name) + 1:
                    user_input = user_input.replace(e_split, names[i])
                else:
                    pass

    ''''''

    max_score = -1
    singer_name = None

    for name in names:
        score = fuzz.partial_ratio(user_input.lower(), name.lower())
        if score > max_score:
            max_score = score
            singer_name = name

    if max_score > 60:
        # 匹配英文单词
        english_words = re.findall(r'[A-Za-z0-9]+', user_input)
        # 将匹配到的英文单词拼接起来
        english_part = ' '.join(english_words)
        # # print('English Part', english_part)
        english_split = english_part.split(' ')
        # # print('Singer', singer_name)
        singer_split = singer_name.split(' ')
        # # print(singer_split)
        for s_split in singer_split:
            for e_split in english_split:
                score = fuzz.partial_ratio(s_split.lower(), e_split.lower())
                if score > 80:
                    # # print(s_split, e_split, score)
                    user_input = user_input.replace(e_split, s_split)
        return user_input, True
    else:
        return user_input, False


def keyword_adjustment_optimized(user_input):
    with open('data/keyword.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    # names_without_space = [name.replace(' ', '') for name in names]

    # 創建名字的小寫版本set以提高查找效率
    names_set = {name.lower() for name in names}

    # 提取用戶輸入中的英文字詞並轉成小寫
    english_words = re.findall(r'[A-Za-z0-9]+', user_input.lower())

    # 基本匹配檢查
    for word in english_words:
        if word in names_set:
            return user_input, True  # 如果找到精確匹配，直接返回

    # 如果基本匹配未找到，進行模糊匹配
    for word in english_words:
        for name in names:
            if fuzz.partial_ratio(word, name.lower()) > 80:
                user_input = user_input.replace(word, name)
                return user_input, True

    return user_input, False  # 如果都沒找到匹配，返回原輸入


# print(keyword_adjustment_optimized("post malone"))


#
# def run_cmdline(model_path: Text) -> None:
#     """Loops over CLI input, passing each message to a loaded NLU model."""
#     agent = Agent.load(model_path)
#
#     print_success("NLU model loaded. Type a message and press enter to parse it.")
#     while True:
#         # print_success("Next message:")
#         try:
#             message = input().strip()
#         except (EOFError, KeyboardInterrupt):
#             print_info("Wrapping up command line chat...")
#             break
#
#         result = asyncio.run(agent.parse_message(message))
#
#         '''
#         輸入句子: 你好
#         print(result['intent'])
#         >> {'name': 'greet', 'confidence': 0.9999651908874512}
#
#         print(result['intent']['name'])
#         >> greet
#         '''
#         # print(result['intent'])
#         # print(json_to_string(result))
#         print('---')
#         print(f'message: {message}')
#         print(f"intent: {result['intent']['name']}")
#         print(f"score: {result['intent']['confidence']}")
#         print('--')
#         # print(result['entities'])
#         if len(result['entities']) == 0:
#             print('No Entities')
#         else:
#             for i in range(len(result['entities'])):
#                 print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
#         print('--')
#         # print(json_to_string(result))


def run_cmdline1(model_path: Text, words) -> None:
    """Loops over CLI input, passing each message to a loaded NLU model."""
    agent = Agent.load(model_path)

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    for word in words:
        print('origi msg:', word)
        # message, find_singer = keyword_adjustment(word)
        message, find_singer = keyword_adjustment_optimized(word)
        print(f'after function: {message}')

        result = asyncio.run(agent.parse_message(message))

        '''
        輸入句子: 你好
        print(result['intent'])
        >> {'name': 'greet', 'confidence': 0.9999651908874512}

        print(result['intent']['name'])
        >> greet 
        '''

        print(f'find singer?', find_singer)  # from function
        print(f"intent: {result['intent']['name']}")
        print(f"score: {result['intent']['confidence']}")
        if result['intent']['confidence'] > 0.6:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('--')
        if len(result['entities']) == 0:
            """
            鄭伊健 (Ekin Cheng) 名字必須分開
            """
            print('No Entities')
        else:
            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")

        print('-----------------------------------------------')


def run_cmdline2(model_path: Text, words) -> None:
    """Loops over CLI input, passing each message to a loaded NLU model."""
    agent = Agent.load(model_path)

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    for word in words:
        message = word
        print('origi msg:', message)
        # message, find_singer = keyword_adjustment(word)
        # message, find_singer = keyword_adjustment_optimized(word)
        # print(f'after function: {message}')

        result = asyncio.run(agent.parse_message(message))

        '''
        輸入句子: 你好
        print(result['intent'])
        >> {'name': 'greet', 'confidence': 0.9999651908874512}

        print(result['intent']['name'])
        >> greet 
        '''

        # print(f'find singer?', find_singer)  # from function
        print(f"intent: {result['intent']['name']}")
        print(f"score: {result['intent']['confidence']}")
        if result['intent']['confidence'] > 0.6:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('--')
        if len(result['entities']) == 0:
            with open('data/keyword.yml', 'r', encoding='utf-8') as f:
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
    'Apink CHOBOM的演唱會資訊'
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
model_path = r'models\nlu-20240501-165733-frayed-acre.tar.gz'

# run_cmdline1(model_path, words1)
# run_cmdline1(model_path, words2)
# run_cmdline1(model_path, words3)
run_cmdline2(model_path, words1)