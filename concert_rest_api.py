# coding: utf-8
import base64
import json
import requests
from pprint import pprint
from y_example_read_json import *

# location_dict = {
#     '新北': 3,
#     '高雄': 4,
#     '台北': 14,
#     '桃園': 15,
#     '台中': 16,
#     '台南': 17,
#     '基隆': 18,
#     '新竹': 19,
#     '苗栗': 20,
#     '彰化': 21,
#     '南投': 22,
#     '雲林': 23,
#     '嘉義': 24,
#     '屏東': 25,
#     '宜蘭': 26,
#     '花蓮': 27,
#     '台東': 28,
#     '金門': 29,
#     '澎湖': 30,
#     '連江': 31,
#     'Taipei': 1,
#     'New Taipei': 32,
#     'Taoyuan': 33,
#     'Taichung': 34,
#     'Hsinchu': 35,
#     'Miaoli': 36,
#     'Changhua': 37,
#     'Nantou': 38,
#     'Yunlin': 39,
#     'Chiayi': 40,
#     'Pingtung': 41,
#     'Yilan': 42,
#     'Hualien': 43,
#     'Taitung': 44,
#     'Kinmen': 45,
#     'Penghu': 46,
#     'Lienchiang': 47,
#     'Keelung': 48,
#     'Kaohsiung': 49,
#     'Tainan': 50,
#     '歌手': 51,
#     'singer': 52
# }

# Init
url = "https://concertinfo.site/wp-json/wp/v2/posts"
username = "user"
password = "EzMf fRIF 7gwd 2O2F 38G0 QheE"
credentials = "{}:{}".format(username, password)
token = base64.b64encode(credentials.encode())

# Header
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Authorization": "Basic {}".format(token.decode("utf-8")),
    "content-type": "application/json",
}


def get_post_data(id):
    post_response = requests.get(f'{url}/{id}')  # 獲得post_id這個頁面的內容
    post_data = post_response.json()
    print(post_data)

    return post_data


def check_availability():
    # Check
    r = requests.get(
        url,
        headers=headers,
    )

    print(r)  # 200


def post_article(title, content, city, category, pin):
    # categories [(中文68 or 英文67) + 城市code]
    categories = []
    if category == 0:
        categories.append(68)  # 演唱會
    elif category == 1:
        categories.append(67)  # concert
    elif category == 2:
        categories.append(51)  # 歌手
    elif category == 3:
        categories.append(52)  # singer

    categories.append(get_city_code(city))

    print(f'in function')
    print(title)
    print(content)
    print(city)
    print(category)
    print(pin)

    # Post info
    post = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": categories
    }

    # Post
    r = requests.post(
        url,
        headers=headers,
        json=post,
    )

    post_id = json.loads(r.text).get('id')
    print(f'post_id = {post_id}')

    with open('concert_pin_postid.txt', 'a', encoding='utf-8') as f:
        f.write(f'{pin}|{post_id}\n')

    # Print
    pprint(r.text)

    return post_id


def update_article(post_id):
    post = {
        "content": f"{get_post_data(post_id)['content']['rendered']}<button id='followButton'>Follow!</button>",
    }

    # Post
    r = requests.post(
        "{}/{}".format(url, post_id),
        headers=headers,
        json=post,
    )

    pprint(r.text)


def delete_article(post_id):
    # Delete
    r = requests.delete(  # <--- change "post" to "delete"
        "{}/{}".format(url, post_id),
        headers=headers,
    )

    pprint(r.text)


# def get_tag_number(text):
#     tags = []
#     for tag, id in location_dict.items():
#         if text.lower() == tag.lower():
#             tags.append(id)
#             print(tags)
#     return tags


def singer_add_link(singer_id, concert_id):
    # text 連結上面想要顯示的文字
    post_response = requests.get(f'{url}/{singer_id}')  # 獲得post_id這個頁面的內容
    post_data = post_response.json()
    print(post_data)

    # 讀取id 獲得concert page的標題 放上去
    link_text = ''

    # Post info
    post = {
        "content": f"{get_post_data(singer_id)['content']['rendered']}<a href='concertinfo.site/?p={concert_id}'>{link_text}</a>",
    }

    r = requests.post(
        "{}/{}".format(url, singer_id),
        headers=headers,
        json=post,
    )


def singer_remove_link(singer_id, concert_id):
    # singer_id 歌手的頁面
    # concert_id 演唱會的頁面
    # text 顯示的文字

    # 讀取id 獲得concert page的標題 放上去
    link_text = 'hello I am Kuan la'

    # "" not ''
    remove_link = f'<p><a href="concertinfo.site/?p={concert_id}">{link_text}</a></p>'
    content = get_post_data(singer_id)['content']['rendered']
    print(content)
    updated_content = content.replace(remove_link, '')
    print(updated_content)

    # Post info
    post = {
        "content": updated_content,
    }

    r = requests.post(
        "{}/{}".format(url, singer_id),
        headers=headers,
        json=post,
    )


# print(get_post_data(104)['content']['rendered'])
# post_article('test',
#              get_post_data(104)['content']['rendered'],
#              1,
#              [4, 5])
''''''
# post = {
#     "content": f"{get_post_data(104)['content']['rendered']}",
# }
#
# # Post
# r = requests.post(
#     "{}/{}".format(url, 165),
#     headers=headers,
#     json=post,
# )
''''''
# singer_add_link(15, 104, 'hello I am Kuan')
# singer_remove_link(15, 104)
# post_article("hello, kuan", "just a test", 0, [3, 4])
# delete_article(107)
# update_article(104)
# http://example.com/?p=ID
# keyword = 'taipei'

# id = post_article("kuan! kuan!", "just a test", 0, get_tag_number("台北"))

# singer_post_id = 15  # singer page
# post_response = requests.get(f'{url}/{singer_post_id}')  # 獲得post_id這個頁面的內容
# post_data = post_response.json()
# print(post_data)
#
# concert_post_id = 104
# # Post info
# post = {
#     "content": f"{post_data['content']['rendered']}<a href='concertinfo.site/?p={concert_post_id}'>New Post Link</a>",
# }
#
# r = requests.post(
#     "{}/{}".format(url, singer_post_id),
#     headers=headers,
#     json=post,
# )

city_code = {
    "新北": 70,
    "台北": 14,
    "桃園": 15,
    "台中": 16,
    "台南": 17,
    "基隆": 18,
    "新竹": 19,
    "苗栗": 20,
    "彰化": 21,
    "南投": 22,
    "雲林": 23,
    "嘉義": 24,
    "屏東": 25,
    "宜蘭": 26,
    "花蓮": 27,
    "台東": 28,
    "金門": 29,
    "澎湖": 30,
    "連江": 31,
    "高雄": 69,
    "Taipei": 1,
    "New Taipei": 32,
    "Taoyuan": 33,
    "Taichung": 34,
    "Hsinchu": 35,
    "Miaoli": 36,
    "Changhua": 37,
    "Nantou": 38,
    "Yunlin": 39,
    "Chiayi": 40,
    "Pingtung": 41,
    "Yilan": 42,
    "Hualien": 43,
    "Taitung": 44,
    "Kinmen": 45,
    "Penghu": 46,
    "Lienchiang": 47,
    "Keelung": 48,
    "Kaohsiung": 49,
    "Tainan": 50,
    "歌手": 51,
    "singer": 52,
    "concert": 67,
    "演唱會": 68
}


def get_city_code(text):
    # 將字典鍵轉換為小寫形式
    lowercase_dict = {key.lower(): value for key, value in city_code.items()}

    # 將要轉換的文字轉換成統一小寫形式
    lower_text = text.lower()

    # 將統一小寫形式的文字轉換成數字，沒有找到就輸出71 (unknown)
    code = lowercase_dict.get(lower_text, 71)

    print(code)

    return code


# title, content, city_name, zh_en_concert_singer, pin
# content = f"""
# <p class="has-palette-color-4-color has-text-color has-link-color">售票: 123456</p>
# <p class="has-palette-color-4-color has-text-color has-link-color">票價: 234123 </p>
# <p class="has-palette-color-4-color has-text-color has-link-color">表演時間： 1234123</p>
# <p class="has-palette-color-4-color has-text-color has-link-color">地點: 1324123</p>
# <p class="has-palette-color-4-color has-text-color has-link-color">系統: 1341</p>
# <p class="has-palette-color-4-color has-text-color has-link-color">網址: 13241234</p>
# """
# post_article('20240404', content, "台北", 0, "12345")

def print_list_str(lst):
    lst_str = ''
    if len(lst) == 1 and lst[0] != '':
        lst_str = lst[0]
    elif len(lst) > 1:
        for i in range(len(lst)):
            lst_str += str(lst[i]) + ' / '
        lst_str = lst_str[:-3]
    else:
        lst_str = '-'

    return lst_str


def test_po():
    for i in range(10):
        # sdt = ''
        # prc = ''
        # pdt = ''
        # loc = ''

        sdt_str = f"售票時間  :  {print_list_str(data[index]['sdt'])}"
        prc_str = f"價格         :  {print_list_str(data[index]['prc'])}"
        pdt_str = f"表演時間  :  {print_list_str(data[index]['pdt'])}"
        loc_str = f"地點         :  {print_list_str(data[index]['loc'])}"
        web_str = f"售票網站  :  {data[index]['web']}"
        url_txt = f"售票網址  :  "
        url_str = f"<a href='{data[index]['url']}' target='_blank'>{data[index]['url']}</a>"

        content = f"""
                <p class="has-palette-color-4-color has-text-color has-link-color">{sdt_str}</p>
                <p class="has-palette-color-4-color has-text-color has-link-color">{prc_str}</p>
                <p class="has-palette-color-4-color has-text-color has-link-color">{pdt_str}</p>
                <p class="has-palette-color-4-color has-text-color has-link-color">{loc_str}</p>
                <p class="has-palette-color-4-color has-text-color has-link-color">{web_str}</p>
                <p class="has-palette-color-4-color has-text-color has-link-color">{url_txt}{url_str}</p>
                """

        post_article(data[i]['tit'], content, data[i]['cit'], 0, data[i]['pin'])


data = read_json("concert_3_14_23.json")

index = 88
sdt = ''
prc = ''
pdt = ''
loc = ''

sdt_str = f"售票時間  :  {print_list_str(data[index]['sdt'])}"
prc_str = f"價格         :  {print_list_str(data[index]['prc'])}"
pdt_str = f"表演時間  :  {print_list_str(data[index]['pdt'])}"
loc_str = f"地點         :  {print_list_str(data[index]['loc'])}"
web_str = f"售票網站  :  {data[index]['web']}"
url_txt = f"售票網址  :  "
url_str = f"<a href='{data[index]['url']}' target='_blank'>{data[index]['url']}</a>"

# content = f"""
#     <div style="white-space: pre-wrap;>
#     <p class="has-palette-color-4-color has-text-color has-link-color"></p>
#     <p class="has-palette-color-4-color has-text-color has-link-color">{sdt_str}</p>
#     <p class="has-palette-color-4-color has-text-color has-link-color">{prc_str}</p>
#     <p class="has-palette-color-4-color has-text-color has-link-color">{pdt_str}</p>
#     <p class="has-palette-color-4-color has-text-color has-link-color">{loc_str}</p>
#     <p class="has-palette-color-4-color has-text-color has-link-color">{web_str}</p>
#     <p class="has-palette-color-4-color has-text-color has-link-color">{url_str}</p>
#     </div>
#     """
''' '''
# content = f"""
#     <div style="white-space: pre-wrap;>
#     <span class="has-palette-color-4-color has-text-color has-link-color"></span>
#     <span class="has-palette-color-4-color has-text-color has-link-color">{sdt_str}</span>
#     <span class="has-palette-color-4-color has-text-color has-link-color">{prc_str}</span>
#     <span class="has-palette-color-4-color has-text-color has-link-color">{pdt_str}</span>
#     <span class="has-palette-color-4-color has-text-color has-link-color">{loc_str}</span>
#     <span class="has-palette-color-4-color has-text-color has-link-color">{web_str}</span>
#     <span class="has-palette-color-4-color has-text-color has-link-color">{url_str}</span>
#     </div>
#     """
''' 目前最佳 '''
content = f"""
        <p class="has-palette-color-4-color has-text-color has-link-color">{sdt_str}</p>
        <p class="has-palette-color-4-color has-text-color has-link-color">{prc_str}</p>
        <p class="has-palette-color-4-color has-text-color has-link-color">{pdt_str}</p>
        <p class="has-palette-color-4-color has-text-color has-link-color">{loc_str}</p>
        <p class="has-palette-color-4-color has-text-color has-link-color">{web_str}</p>
        <p class="has-palette-color-4-color has-text-color has-link-color">{url_txt}{url_str}</p>
        """
''' 目前最佳 '''
# post_article(data[index]['tit'], content, data[index]['cit'], 0, data[index]['pin'])
test_po()
# <span class="has-palette-color-4-color has-text-color has-link-color"></span>
# <p class="has-palette-color-4-color has-text-color has-link-color">{url_str}</p>
