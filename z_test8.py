# coding: utf-8
import base64
import json
import requests
from pprint import pprint

location_dict = {
    '新北': 3,
    '高雄': 4,
    '台北': 14,
    '桃園': 15,
    '台中': 16,
    '台南': 17,
    '基隆': 18,
    '新竹': 19,
    '苗栗': 20,
    '彰化': 21,
    '南投': 22,
    '雲林': 23,
    '嘉義': 24,
    '屏東': 25,
    '宜蘭': 26,
    '花蓮': 27,
    '台東': 28,
    '金門': 29,
    '澎湖': 30,
    '連江': 31,
    'Taipei': 1,
    'New Taipei': 32,
    'Taoyuan': 33,
    'Taichung': 34,
    'Hsinchu': 35,
    'Miaoli': 36,
    'Changhua': 37,
    'Nantou': 38,
    'Yunlin': 39,
    'Chiayi': 40,
    'Pingtung': 41,
    'Yilan': 42,
    'Hualien': 43,
    'Taitung': 44,
    'Kinmen': 45,
    'Penghu': 46,
    'Lienchiang': 47,
    'Keelung': 48,
    'Kaohsiung': 49,
    'Tainan': 50,
    '歌手': 51,
    'singer': 52
}

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


def post_article(title, content, status, categories):
    if status == 0:
        status = "draft"
    elif status == 1:
        status = "publish"

    # Post info
    post = {
        "title": title,
        "content": content,
        "status": status,
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


def get_tag_number(text):
    tags = []
    for tag, id in location_dict.items():
        if text.lower() == tag.lower():
            tags.append(id)
            print(tags)
    return tags


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
post = {
        "content": f"{get_post_data(104)['content']['rendered']}",
    }

# Post
r = requests.post(
    "{}/{}".format(url, 165),
    headers=headers,
    json=post,
)
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
