import asyncio
import logging
from typing import Text

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from fuzzywuzzy import fuzz
import yaml
import re

from duckling import *

d = DucklingWrapper(language=Language.CHINESE)


def find_singer_name(user_input):
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


def run_cmdline(model_path: Text) -> None:
    """Loops over CLI input, passing each message to a loaded NLU model."""
    agent = Agent.load(model_path)

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    while True:
        # print_success("Next message:")
        try:
            message = input().strip()
            duckling_result = d.parse_time(message)
            if duckling_result:
                print(duckling_result[0]['value'])
            else:
                print('Duckling None')

        except (EOFError, KeyboardInterrupt):
            print_info("Wrapping up command line chat...")
            break

        result = asyncio.run(agent.parse_message(message))

        print(result)
        '''
        輸入句子: 你好
        print(result['intent'])
        >> {'name': 'greet', 'confidence': 0.9999651908874512}

        print(result['intent']['name'])
        >> greet 
        '''
        # print(result['intent'])
        # print(json_to_string(result))
        print('---')
        print(f'message: {message}')
        print(f"intent: {result['intent']['name']}")
        print(f"score: {result['intent']['confidence']}")
        print('--')
        # print(result['entities'])
        if len(result['entities']) == 0:
            print('No Entities')
        else:
            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
        print('--')
        # print(json_to_string(result))


def run_cmdline1(model_path: Text, words) -> None:
    """Loops over CLI input, passing each message to a loaded NLU model."""
    agent = Agent.load(model_path)

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    for index, word in enumerate(words):
        # message, find_singer = find_singer_name(word)
        message = word.lower()
        print(f'ori msg: {message}')
        # print(d.parse_time(message))

        result = asyncio.run(agent.parse_message(message))

        '''
        輸入句子: 你好
        print(result['intent'])
        >> {'name': 'greet', 'confidence': 0.9999651908874512}

        print(result['intent']['name'])
        >> greet 
        '''

        print(f'message: {message}')
        # print(f'find singer?', find_singer)
        print(f"intent: {result['intent']['name']}")
        print(f"score: {result['intent']['confidence']}")
        if result['intent']['confidence'] > 0.6:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('--')
        if len(result['entities']) == 0:
            print('No Entities')
        else:
            keywords = []
            for i in range(len(result['entities'])):
                if result['entities'][i]['entity'] != 'keyword' and result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                elif result['entities'][i]['entity'] == 'keyword':
                    keywords.append(result['entities'][i]['value'])
            singer_name = max(keywords, key=len)
            # print(type(singer_name))
            # print(f"singer name = {singer_name.title()}")

            with open('data/keyword.yml', 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
            names = [name.replace(' ', '') for name in names]

            found = False
            for j, name in enumerate(names):
                if name.lower() == singer_name.lower():
                    singer_name = names[j]
                    found = True
                    break
            if not found:
                singer_name = singer_name.title()
            print(f"singer name = {singer_name}")



            # keywords = []
            # for i in range(len(result['entities'])):
            #     if result['entities'][i]['entity'] == 'keyword' and result['entities'][i]['value']:
            #         keywords.append(result['entities'][i]['value'])
            # singer_name = max(keywords, key=len)
            # print(type(singer_name))
            # print(singer_name)

        print('-----------------------------------------------')



logger = logging.getLogger(__name__)
#
# words1 = [
#     'Post Malone',
#     'Post Malone 演唱會',
#     '演唱會 post malone',
#     'ive 演唱會',
#     '演唱會 IVE',
#     'newjeans',
#     'NewJeans 演唱會',
#     '演唱會 NewJeans',
#     'Le Sserafim',
#     'LE SSERAFIM 演唱會',
#     '台北 演唱會',
#     '桃園 下周',
#     '下個月 新北',
#     '請告訴我有關IVE演唱會的資訊',
#     '爵士音樂',
#     '爵士樂',
#     '請問這位歌手的演唱會將在哪個城市舉行？',
#     'IVE',
#     'stayc',
#     'aespa',
#     'wheein',
#     '如果我想知道這個週末在台北以外的城市有哪些饒舌演唱會，該怎麼查詢？',
#     '明天在台北的饒舌演唱會之外，後天在其他城市有類似活動嗎？',
#     'ziont',
#     '那麼後天呢？在台北或其他城市有類似的饒舌演唱會嗎？',
#     '鄧福如',
#     'postmalone',
#     'taylorswift',
#     '請問台北明天有什麼演唱會?',
#     '請問IVE是幾點開始搶票?',
#     '下周五之前的搶票時間',
#     'postmalone'
# ]
# words2 = [
#     '那麼下周呢',
#     '那台北呢',
#     '那下個月呢',
#     '如果是後天呢',
# ]
# words3 = [
#     '明天有哪些演唱會開始售票?',
#     '後天 演唱會 售票',
#     '告訴我tarlorswift演唱會的資訊',
#     '下周搶票資訊',
#     '花蓮 明天',
#     '明天 花蓮',
#     '新北 下個月',
#     '下個月 新北',
#     '下個月 新北 演唱會',
#     '新北 下個月 演唱會',
#     '下周在高雄的演唱會有哪些',
#     '下周晚上 在高雄有哪些演唱會?',
#     '我想請問一下againstthecurrent的演唱會'
# ]
# words4 = [
#     "演唱會是在哪個地點舉行的？",
#     "有沒有關於演唱會的詳細時間表？",
#     "演唱會的門票價格是多少？",
#     "我可以在哪裡購買演唱會的門票？",
#     "演唱會的座位有什麼選擇？",
#     "有關演唱會場地的停車信息嗎？",
#     "有什麼注意事項或規定我需要知道嗎？",
#     "演唱會的安全措施是什麼？",
#     "我需要攜帶什麼東西參加演唱會？",
#     "演唱會將提供飲食或飲料嗎？",
#     "有沒有關於演唱會的禁止物品清單？",
#     "演唱會的表演者是誰？",
#     "演唱會的音樂類型是什麼？",
#     "演唱會會持續多長時間？",
#     "是否有任何開場表演或特別嘉賓？",
#     "我可以攜帶相機或錄音設備嗎？",
#     "演唱會的服裝規定是什麼？",
#     "演唱會提供殘障人士的設施嗎？",
#     "是否有年齡限制參加演唱會？",
#     "演唱會的氛圍是如何的？",
#     "是否有站立區和座位區的區別？",
#     "演唱會的場地有多大？",
#     "演唱會會提供紀念品或周邊商品嗎？",
#     "有關於演唱會的網絡規定嗎？",
#     "我可以攜帶包包進入演唱會場地嗎？",
#     "有沒有任何推薦的交通方式到達演唱會場地？",
#     "是否有提供演唱會的公共交通信息？",
#     "演唱會的舞台設計是什麼樣的？",
#     "演唱會的燈光和音響效果如何？",
#     "演唱會的主辦方是誰？",
#     "有沒有任何取消或延期的風險？",
#     "我需要提前到場多久？",
#     "演唱會有沒有定時休息或中場休息？",
#     "演唱會的場地是否提供飲用水？",
#     "是否有任何特別的紀念品活動或活動？",
#     "演唱會的場地是否提供設施給小孩或家庭？",
#     "我可以在演唱會場地附近找到哪些餐廳或食物選擇？",
#     "有沒有推薦的住宿選擇？",
#     "演唱會有沒有可能出現人潮擁擠的情況？",
#     "是否有任何關於演唱會的社交媒體活動或標籤？",
#     "我可以在演唱會上與藝人互動嗎？",
#     "演唱會是否提供VIP或特別座位？",
#     "有沒有關於演唱會的退票政策？",
#     "我需要提供身份證明或門票以進入場地嗎？",
#     "演唱會是否有提供多語言的服務？",
#     "我可以在演唱會上攜帶自己的食物或飲料嗎？",
#     "是否有任何關於演唱會的慈善或社區參與活動？",
#     "演唱會的音樂設備是否支持聽力輔助裝置？",
#     "是否有任何關於演唱會的家庭友好性質？",
#     "演唱會的主題或概念是什麼？",
# ]

words1 = [
    'IVE',
    'hip hop taipei',
    'could you tell me any boombap concerts in taipei?'
]

model_path = r'models\nlu-20240505-013208-fixed-itinerary.tar.gz'

# run_cmdline1(model_path, words1)
# run_cmdline1(model_path, words2)
# run_cmdline1(model_path, words4)
# run_cmdline(model_path)

with open('z_test1.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
lines = [line.replace('\n', '') for line in lines]
run_cmdline1(model_path, lines)
