# coding: utf-8
import base64
import json
import requests
from pprint import pprint
from y_example_read_json import *
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re
from datetime import datetime, timedelta

url = "https://concertinfo.site/wp-json/wp/v2/posts"
username = "user"
password = "EzMf fRIF 7gwd 2O2F 38G0 QheE"
credentials = "{}:{}".format(username, password)
token = base64.b64encode(credentials.encode())

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

# '<!-- wp:html -->
# '<!-- /wp:html -->

# Header
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Authorization": "Basic {}".format(token.decode("utf-8")),
    "content-type": "application/json",
}


def check_availability():
    # Check
    r = requests.get(
        url,
        headers=headers,
    )

    print(r)  # 200


def print_list_str(lst):
    """ list 所有元素用str輸出 """
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


def replace_time(text):
    pattern = r'\d{2}:\d{2}'  # 匹配時間的正則表達式模式
    text = re.sub(pattern, '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()  # 去除首尾空格


def format_date(date_str):
    parts = date_str.split('-')
    month = parts[1].zfill(2)  # 用 zfill(2) 將月份填充成兩位數
    day = parts[2].zfill(2)  # 用 zfill(2) 將日期填充成兩位數
    return f"{parts[0]}-{month}-{day}"


def generate_date_range(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    date_range = []
    current_date = start_date

    while current_date <= end_date:
        date_range.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_range


def get_city_code(text):
    # 將字典鍵轉換為小寫形式
    lowercase_dict = {key.lower(): value for key, value in city_code.items()}

    # 將要轉換的文字轉換成統一小寫形式
    lower_text = text.lower()

    # 將統一小寫形式的文字轉換成數字，沒有找到就輸出71 (unknown)
    code = lowercase_dict.get(lower_text, 71)

    print(code)

    return code


def delete_article(post_id):
    # Delete
    r = requests.delete(  # <--- change "post" to "delete"
        "{}/{}".format(url, post_id),
        headers=headers,
    )

    pprint(r.text)


def update_article_content(post_id, content):
    post = {
        "content": content,
    }

    # Post
    r = requests.post(
        "{}/{}".format(url, post_id),
        headers=headers,
        json=post,
    )

    pprint(r.text)


def get_post_content(id):
    post_response = requests.get(f'{url}/{id}')  # 獲得post_id這個頁面的內容
    post_data = post_response.json()
    content = post_data['content']['rendered']

    return content


def post_singer(data):
    categories = [51]

    singer_name = data['singer_name']
    singer_page_url = data['singer_page_url']  # 暫時用不到

    if data['singer_image_page_url'] != '-':
        print('擁有圖片')
        singer_image_page_url = data['singer_image_page_url']
        jpg_url = data['jpg_url']
        provider_name = data['provider_name']
        image_name = data['image_name']
        cc = data['cc']
    else:
        print('沒有圖片')
        singer_image_page_url = "https://www.vecteezy.com/free-vector/microphone"
        jpg_url = 'http://concertinfo.site/wp-content/uploads/2024/04/vecteezy_microphone-line-art-illustration-on-black-background_7059740.jpg'
        provider_name = '-'
        image_name = '-'
        cc = '-'

    content = f"""
    <!-- wp:html -->
    <style>
    /* 针对图片卡片的样式 */
    .image-card {{
        border: 1px solid #ccc;
        display: flex; /* 使用flex布局 */
        justify-content: space-between; /* 确保左侧内容和图片在右侧分开 */
        align-items: flex-start; /* 标题对齐到顶部 */
        max-width: 400px; /* 与邮件表单的最大宽度相同 */
        margin: 20px auto; /* 居中显示，与邮件表单相同的外边距 */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 相同的阴影效果 */
        border-radius: 10px; /* 圆角边框 */
        overflow: hidden; /* 超出边界的图片部分会被隐藏 */
        padding: 20px;
    }}
    .image-card img {{
        width: 300px; /* 图片宽度设置为300像素 */
        height: 400px; /* 图片高度设置为300像素 */
        display: block; /* 避免底部有空隙 */
        object-fit: cover; /* 调整图片大小以覆盖整个设定区域，可能会裁剪部分图片 */
    }}
    .image-card .content {{
        display: flex; /* 使用flex布局 */
        flex-direction: column; /* 元素垂直排列 */
        flex: 1; /* 允许内容区域成长填充可用空间 */
        justify-content: center; /* 中心对齐所有子元素 */
        margin-right: 20px; /* 右邊距，增加间隔 */
        text-align: center; /* 文本居中 */
    }}
    .image-card h1 {{
        margin: 0 0 10px 0; /* 移除默认的外边距并添加下方间隔 */
        font-size: 30px; /* 设置字体大小为30px */
    }}
    .concert-box {{
        border: 1px solid #ccc;
        padding: 10px 50px 10px 10px; /* 右侧内边距增加 */
        width: 100%; /* 宽度调整为100%以填充父元素宽度 */
        text-align: left; /* 将文本对齐设置为左对齐 */
        font-size: 20px; /* 字体大小 */
        margin-top: 10px; /* 上方外边距 */
    }}
    .concert-link {{ /* 适用于链接的样式 */
        color: white; /* 继承文字颜色 */
        padding-left: 10px; /* 链接内容距离左边框的距离 */
        text-decoration: none; /* 去除下划线 */
        display: block; /* 让链接填满整个框框 */
    }}
    .image-container {{
        display: flex; /* 使用flex布局 */
        flex-direction: column; /* 元素垂直排列 */
        align-items: center; /* 内容居中对齐 */
        width: 300px; /* 限制容器宽度与图片宽度相同 */
    }}
    .image-container p {{
        word-wrap: break-word; /* 允许单词在超出容器宽度时断行 */
        text-align: center; /* 文本居中显示 */
        margin: 5px 0; /* 设置上下外边距为5像素，左右为0 */
    }}
    .author {{
        margin-top: 15px; /* 增加与图片的间隔 */
    }}
    .date-span {{
        background-color: #f2f2f2; /* 背景色 */
        color: black; /* 文字颜色 */
        padding: 3px 6px; /* 内边距 */
        margin-right: 10px; /* 右侧与后续文本间隔 */
        margin-top: 10px; /* 顶部外边距 */
        margin-bottom: 10px; /* 底部外边距 */
        border-radius: 4px; /* 边角圆滑 */
        font-weight: bold; /* 字体加粗 */
        display: inline-block; /* 设置为内联块级元素 */
    }}
    </style>
    <div class="image-card">
        <div class="content">
            <h1>即將來臨的演唱會</h1>
        </div>
        <div class="image-container">
                    <a href="{singer_image_page_url}">
                <img src="{jpg_url}" alt="{singer_name}" />
            </a>
                    <p class="author">作者：{provider_name}</p>
            <p>授權：{cc}</p>
            <p>來源：{image_name}</p>
        </div>
    </div>
    <!-- /wp:html -->
    """
    print(content)

    '''
    <div class="concert-box">
        <a href="https://example.com/concert1" class="concert-link"><span class="date-span">11/9</span> CONCERT1</a>
    </div>
    '''
    # Post info
    post = {
        "title": data['singer_name'],
        "content": content,
        "status": "publish",
        "categories": categories,
    }

    # Post
    r = requests.post(
        url,
        headers=headers,
        json=post,
    )

    # Print
    pprint(r.text)


def singer_add_concert(id, data):
    content = get_post_content(id)
    new_concert = f"""
    <div class="concert-box">
            <a href="{data['url']}" class="concert-link"><span class="date-span">{data['pdt'][0]}</span>{data['tit']}</a>
        </div>
    """
    former = "<!-- wp:html -->" + content.split('<h1>即將來臨的演唱會</h1>')[0] + "<h1>即將來臨的演唱會</h1>"
    latter =  new_concert + content.split('<h1>即將來臨的演唱會</h1>')[1] + "<!-- /wp:html -->"
    print(former)
    print('-------')
    print(latter)
    content = former + latter
    update_article_content(id, content)


def post_concert(data):
    sdt_str = f"售票時間  :  {print_list_str(data['sdt'])}"
    prc_str = f"價格         :  {print_list_str(data['prc'])}"
    pdt_str = f"表演時間  :  {print_list_str(data['pdt'])}"
    loc_str = f"地點         :  {print_list_str(data['loc'])}"
    web_str = f"售票網站  :  {data['web']}"
    url_str = f"售票網址  :  <a href='{data['url']}' target='_blank'>{data['url']}</a>"

    content = f"""
            <!-- wp:html -->
            <div style="white-space: pre-wrap;">
                <p class="has-palette-color-4-color has-text-color has-link-color">
                    {sdt_str}<br>
                    {prc_str}<br>
                    {pdt_str}<br>
                    {loc_str}<br>
                    {web_str}<br>
                    {url_str}
                </p>
            </div>
            <!-- /wp:html -->
            """

    categories = [68]  # 演唱會
    if data['cit'] != '':
        categories.append(get_city_code(data['cit']))

    if data['pdt']:
        date = replace_time(data['pdt'][0]).replace('/', '-')

        if '~' not in date:
            date = format_date(date)
            concert_dates = [{"concert_date": date}]
        else:
            date = f"{format_date(date.split(' ~ ')[0])} ~ {date.split(' ~ ')[1]}"
            date_range = generate_date_range(date.split(' ~ ')[0], date.split(' ~ ')[1])
            concert_dates = []
            for i in range(len(date_range)):
                concert_dates.append({f"concert_date": date_range[i]})

        # Post info
        post = {
            "title": data['tit'],
            "content": content,
            "status": "publish",
            "categories": categories,
            "fields": {
                "concert_dates": concert_dates
            }
            # "fields": {  # 添加自定義字段部分
            #     "concert_date": "2024-04-20"

            # "fields": {
            #     "concert_dates": [
            #         {"concert_date": "2024-04-01"},
            #         {"concert_date": "2024-04-02"},
            #     ]
            # }
        }
    else:
        # Post info
        post = {
            "title": data['tit'],
            "content": content,
            "status": "publish",
            "categories": categories,
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
        f.write(f"{post_id}|||{data['pin']}\n")

    # Print
    pprint(r.text)


# def post_concert(title, content, date, city, pin):  # 倒數第二個argument, 0 演唱會, 1 歌手
#     # categories [(中文68 or 英文67) + 城市code]
#
#     categories = [68]  # 演唱會
#     if city != '':
#         categories.append(get_city_code(city))
#
#     # if category == 0:
#     #     categories.append(68)  # 演唱會
#     # elif category == 1:
#     #     categories.append(67)  # concert
#     # elif category == 2:
#     #     categories.append(51)  # 歌手
#     # elif category == 3:
#     #     categories.append(52)  # singer
#
#     print(f'in function')
#     print(title)
#     print(content)
#     print(date)
#     print(city)
#     print(pin)
#
#     # Post info
#     post = {
#         "title": title,
#         "content": content,
#         "status": "publish",
#         "categories": categories,
#         # "fields": {  # 添加自定義字段部分
#         #     "concert_date": "2024-04-20"
#         "fields": {
#             "follow_emails": [
#                 {"follow_email: 'pfii1997119@gmail.com'"}
#             ]
#         }
#     }
#
#     # post = {
#     #     "title": "測試la",
#     #     "content": content1,
#     #     "status": "publish",
#     #     "categories": 68,
#
#     # Post
#     r = requests.post(
#         url,
#         headers=headers,
#         json=post,
#     )
#
#     post_id = json.loads(r.text).get('id')
#     print(f'post_id = {post_id}')
#
#     with open('concert_pin_postid.txt', 'a', encoding='utf-8') as f:
#         f.write(f'{post_id}|||{pin}\n')
#
#     # Print
#     pprint(r.text)
#
#     # return post_id


# '<!-- wp:html -->
# '<!-- /wp:html -->
# post_data = get_post_data(2019)
# print(post_data['content']['rendered'])


# def post_article(title, content, city, category, pin):
#     # categories [(中文68 or 英文67) + 城市code]
#     categories = []
#     if category == 0:
#         categories.append(68)  # 演唱會
#     elif category == 1:
#         categories.append(67)  # concert
#     elif category == 2:
#         categories.append(51)  # 歌手
#     elif category == 3:
#         categories.append(52)  # singer
#
#     categories.append(get_city_code(city))
#
#     print(f'in function')
#     print(title)
#     print(content)
#     print(city)
#     print(category)
#     print(pin)
#
#     # Post info
#     post = {
#         "title": title,
#         "content": content,
#         "status": "publish",
#         "categories": categories
#     }
#
#     # Post
#     r = requests.post(
#         url,
#         headers=headers,
#         json=post,
#     )
#
#     post_id = json.loads(r.text).get('id')
#     print(f'post_id = {post_id}')
#
#     with open('concert_pin_postid.txt', 'a', encoding='utf-8') as f:
#         f.write(f'{pin}|{post_id}\n')
#
#     # Print
#     pprint(r.text)
#
#     return post_id


# def get_tag_number(text):
#     tags = []
#     for tag, id in location_dict.items():
#         if text.lower() == tag.lower():
#             tags.append(id)
#             print(tags)
#     return tags


# def singer_add_link(singer_id, concert_id):
#     # text 連結上面想要顯示的文字
#     post_response = requests.get(f'{url}/{singer_id}')  # 獲得post_id這個頁面的內容
#     post_data = post_response.json()
#     print(post_data)
#
#     # 讀取id 獲得concert page的標題 放上去
#     link_text = ''
#
#     # Post info
#     post = {
#         "content": f"{get_post_data(singer_id)['content']['rendered']}<a href='concertinfo.site/?p={concert_id}'>{link_text}</a>",
#     }
#
#     r = requests.post(
#         "{}/{}".format(url, singer_id),
#         headers=headers,
#         json=post,
#     )


# def singer_remove_link(singer_id, concert_id):
#     # singer_id 歌手的頁面
#     # concert_id 演唱會的頁面
#     # text 顯示的文字
#
#     # 讀取id 獲得concert page的標題 放上去
#     link_text = 'hello I am Kuan la'
#
#     # "" not ''
#     remove_link = f'<p><a href="concertinfo.site/?p={concert_id}">{link_text}</a></p>'
#     content = get_post_data(singer_id)['content']['rendered']
#     print(content)
#     updated_content = content.replace(remove_link, '')
#     print(updated_content)
#
#     # Post info
#     post = {
#         "content": updated_content,
#     }
#
#     r = requests.post(
#         "{}/{}".format(url, singer_id),
#         headers=headers,
#         json=post,
#     )


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


# def test_po():
#     for i in range(10):
#         # sdt = ''
#         # prc = ''
#         # pdt = ''
#         # loc = ''
#
#         sdt_str = f"售票時間  :  {print_list_str(data[index]['sdt'])}"
#         prc_str = f"價格         :  {print_list_str(data[index]['prc'])}"
#         pdt_str = f"表演時間  :  {print_list_str(data[index]['pdt'])}"
#         loc_str = f"地點         :  {print_list_str(data[index]['loc'])}"
#         web_str = f"售票網站  :  {data[index]['web']}"
#         url_txt = f"售票網址  :  "
#         url_str = f"<a href='{data[index]['url']}' target='_blank'>{data[index]['url']}</a>"
#
#         content = f"""
#                 <p class="has-palette-color-4-color has-text-color has-link-color">{sdt_str}</p>
#                 <p class="has-palette-color-4-color has-text-color has-link-color">{prc_str}</p>
#                 <p class="has-palette-color-4-color has-text-color has-link-color">{pdt_str}</p>
#                 <p class="has-palette-color-4-color has-text-color has-link-color">{loc_str}</p>
#                 <p class="has-palette-color-4-color has-text-color has-link-color">{web_str}</p>
#                 <p class="has-palette-color-4-color has-text-color has-link-color">{url_txt}{url_str}</p>
#                 """
#
#         post_article(data[i]['tit'], content, data[i]['cit'], 0, data[i]['pin'])


# data = read_json("concert_4_15_1.json")
# post_concert(data[1])

# for i in range(1):
#     title = data[i]['tit']
#     sdt_str = f"售票時間  :  {print_list_str(data[i]['sdt'])}"
#     prc_str = f"價格         :  {print_list_str(data[i]['prc'])}"
#     pdt_str = f"表演時間  :  {print_list_str(data[i]['pdt'])}"
#     loc_str = f"地點         :  {print_list_str(data[i]['loc'])}"
#     web_str = f"售票網站  :  {data[i]['web']}"
#     url_str = f"售票網址  :  <a href='{data[i]['url']}' target='_blank'>{data[i]['url']}</a>"
#
#     content = f"""
#         <!-- wp:html -->
#         <div style="white-space: pre-wrap;">
#             <p class="has-palette-color-4-color has-text-color has-link-color">
#                 {sdt_str}<br>
#                 {prc_str}<br>
#                 {pdt_str}<br>
#                 {loc_str}<br>
#                 {web_str}<br>
#                 {url_str}
#             </p>
#         </div>
#         <!-- /wp:html -->
#         """
#
#     post_concert(title, content, data[i]['cit'], data[i]['pdt'], data[i]['pin'])


# index = 100
#
# title = data[index]['tit']
# sdt_str = f"售票時間  :  {print_list_str(data[index]['sdt'])}"
# prc_str = f"價格         :  {print_list_str(data[index]['prc'])}"
# pdt_str = f"表演時間  :  {print_list_str(data[index]['pdt'])}"
# loc_str = f"地點         :  {print_list_str(data[index]['loc'])}"
# web_str = f"售票網站  :  {data[index]['web']}"
# url_str = f"售票網址  :  <a href='{data[index]['url']}' target='_blank'>{data[index]['url']}</a>"
#
# content = f"""
#     <!-- wp:html -->
#     <div style="white-space: pre-wrap;">
#         <p class="has-palette-color-4-color has-text-color has-link-color">
#             {sdt_str}<br>
#             {prc_str}<br>
#             {pdt_str}<br>
#             {loc_str}<br>
#             {web_str}<br>
#             {url_str}
#         </p>
#     </div>
#     <!-- /wp:html -->
#     """
#
# # Post info
# post = {
#     "title": title,
#     "content": content,
#     "status": "publish",
#     "categories": 68,
#     "fields": {  # 添加自定義字段部分
#         "concert_date": "2024-04-30"
#     }
# }

# # Post
# r = requests.post(
#     url,
#     headers=headers,
#     json=post,
# )

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
# content = f"""
#         <p class="has-palette-color-4-color has-text-color has-link-color">{sdt_str}</p>
#         <p class="has-palette-color-4-color has-text-color has-link-color">{prc_str}</p>
#         <p class="has-palette-color-4-color has-text-color has-link-color">{pdt_str}</p>
#         <p class="has-palette-color-4-color has-text-color has-link-color">{loc_str}</p>
#         <p class="has-palette-color-4-color has-text-color has-link-color">{web_str}</p>
#         <p class="has-palette-color-4-color has-text-color has-link-color">{url_txt}{url_str}</p>
#         """
''' 目前最佳 '''
# post_article(data[index]['tit'], content, data[index]['cit'], 0, data[index]['pin'])
# test_po()
# <span class="has-palette-color-4-color has-text-color has-link-color"></span>
# <p class="has-palette-color-4-color has-text-color has-link-color">{url_str}</p>

''''''
'''
content = """
<style>
/* 针对图片卡片的样式 */
.image-card {
    border: 1px solid #ccc;
    display: block; /* 使链接成为块级元素 */
    max-width: 400px; /* 与邮件表单的最大宽度相同 */
    margin: 20px auto; /* 居中显示，与邮件表单相同的外边距 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 相同的阴影效果 */
    border-radius: 10px; /* 圆角边框 */
    overflow: hidden; /* 超出边界的图片部分会被隐藏 */
}

.image-card img {
    width: 100%; /* 让图片填满容器 */
    display: block; /* 避免底部有空隙 */
    height: auto; /* 保持图片的原始比例 */
}
</style>

<a href="https://concertinfo.site" class="image-card">
    <img src="https://fileinfo.com/img/ss/xl/jpg_44-2.jpg" alt="Singer Name" />
</a>

"""
'''

# # Post info
# post = {
#     "title": "測試la",
#     "content": content1,
#     "status": "publish",
#     "categories": 68,
#     "fields": {  # 添加自定義字段部分
#             "concert_date": "2024-04-20"
#     }
# }

# # Post
# r = requests.post(
#     url,
#     headers=headers,
#     json=post,
#     params={"raw": "true"}  # Adding raw parameter to the request
# )

# post_id = json.loads(r.text).get('id')
# print(f'post_id = {post_id}')
# link = json.loads(r.text).get('link')
# print(f'link = {link}')
# with open('concert_pin_postid.txt', 'a', encoding='utf-8') as f:
#     f.write(f'{pin}|{post_id}\n')

# # Print
# pprint(r.text)

''''''

# content1 = '''
# <div style="border: 1px solid black; padding: 10px;">
#   <h2>这是一个HTML方块</h2>
#   <p>这里是内容...</p>
# </div>
# '''
# content2 = '''
# '<!-- wp:html -->
# <style>
# /* 针对图片卡片的样式 */
# .image-card {
#     border: 1px solid #ccc;
#     display: flex; /* 使用flex布局 */
#     justify-content: space-between; /* 确保左侧内容和图片在右侧分开 */
#     align-items: flex-start; /* 标题对齐到顶部 */
#     max-width: 400px; /* 与邮件表单的最大宽度相同 */
#     margin: 20px auto; /* 居中显示，与邮件表单相同的外边距 */
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 相同的阴影效果 */
#     border-radius: 10px; /* 圆角边框 */
#     overflow: hidden; /* 超出边界的图片部分会被隐藏 */
#     padding: 20px;
# }
# .image-card img {
#     width: 300px; /* 图片宽度设置为300像素 */
#     height: 300px; /* 图片高度设置为300像素 */
#     display: block; /* 避免底部有空隙 */
#     object-fit: cover; /* 调整图片大小以覆盖整个设定区域，可能会裁剪部分图片 */
# }
# .image-card .content {
#     display: flex; /* 使用flex布局 */
#     flex-direction: column; /* 元素垂直排列 */
#     flex: 1; /* 允许内容区域成长填充可用空间 */
#     justify-content: center; /* 中心对齐所有子元素 */
#     margin-right: 20px; /* 右邊距，增加间隔 */
#     text-align: center; /* 文本居中 */
# }
# .image-card h1 {
#     margin: 0 0 10px 0; /* 移除默认的外边距并添加下方间隔 */
#     font-size: 30px; /* 设置字体大小为30px */
# }
# .concert-box {
#     border: 1px solid #ccc; /* 添加边框 */
#     padding: 10px 50px 10px 10px; /* 右侧内边距增加 */
#     width: 100%; /* 宽度调整为100%以填充父元素宽度 */
#     text-align: center; /* 文本居中 */
#     font-size: 20px; /* 字体大小 */
#     margin-top: 10px; /* 上方外边距 */
# }
# .concert-link { /* 适用于链接的样式 */
#     color: inherit; /* 继承文字颜色 */
#     text-decoration: none; /* 去除下划线 */
#     display: block; /* 让链接填满整个框框 */
# }
# </style>
# <div class="image-card">
#     <div class="content">
#         <h1>即將來臨的演唱會</h1>
#         <div class="concert-box">
#             <a href="https://example.com/concert1" class="concert-link">CONCERT1</a>
#         </div>
#         <div class="concert-box">
#             <a href="https://example.com/concert2" class="concert-link">CONCERT2</a>
#         </div>
#     </div>
#     <img src="alarm2.jpg" alt="Singer Name" />
# </div>
#
# <style>
# /* 针对特定表单的卡片容器样式 */
# .emailSignupForm {
#     border: 1px solid #ccc;
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#     padding: 20px;
#     background-color: #101010;
#     max-width: 400px;
#     margin: 20px auto;
#     font-family: Arial, sans-serif;
#     color: white;
#     border-radius: 10px;
#     display: flex; /* 使用 flex 布局 */
#     flex-direction: column; /* 垂直方向排列 */
# }
#
# .emailSignupForm h1, .emailSignupForm p {
#     text-align: center;
#     margin-bottom: 20px;
# }
#
# .emailSignupForm label {
#     display: block;
#     margin-bottom: 10px;
#     color: white;
# }
#
# .emailSignupForm #emailContainer {
#     display: flex; /* 使用 flex 布局 */
#     align-items: center; /* 垂直居中对齐 */
# }
#
# .emailSignupForm label {
#     margin-right: 10px; /* 左侧文字与输入框之间的间隔 */
# }
#
# .emailSignupForm input[type=email], .emailSignupForm input[type=button] {
#     flex: 1; /* 使用 flex-grow 让输入框占据剩余空间 */
#     padding: 10px;
#     margin-bottom: 20px;
#     border: 1px solid #ccc;
#     border-radius: 10px;
# }
#
# .emailSignupForm input[type=button] {
#     background-color: #fe5532;
#     color: white;
#     border: none;
#     cursor: pointer;
# }
#
# .emailSignupForm input[type=button]:hover {
#     background-color: #993333;
# }
#
# .emailSignupForm #successMessage {
#     background-color: #28a745;
#     color: white;
#     text-align: center;
#     padding: 15px;
#     border-radius: 10px;
#     display: none;
# }
# </style>
#
# <form class="emailSignupForm">
#     <h1>Ticket Alarm!</h1> <!-- 第一行文字 -->
#     <p>輸入你的email，隨時接收這位藝人的最新消息!</p> <!-- 第二行描述文字 -->
#     <div id="emailContainer">
#         <label for="emailInput">Enter Email Address</label> <!-- 邮箱输入的标签 -->
#         <input type="email" id="emailInput" name="email" autocomplete="email" multiple=""> <!-- 邮箱输入框，支持自动完成 -->
#     </div>
#     <input type="button" id="useremail" value="Submit" onclick="changeButtonText()"> <!-- 提交按钮，点击时触发JavaScript函数 -->
#     <div id="successMessage" style="display:none;">已成功訂閱！感謝您的訂閱。</div> <!-- 成功消息容器，默认隐藏 -->
#     <script src="/wp-content/themes/blocksy/static/js/email-script.js"></script> <!-- 引入外部JavaScript文件 -->
#     <script>
#         function changeButtonText() {
#             var button = document.getElementById('useremail'); // 获取按钮元素
#             button.style.display = 'none'; // 隐藏按钮
#             var emailContainer = document.getElementById('emailContainer'); // 获取邮箱容器元素
#             emailContainer.style.display = 'none'; // 隐藏邮箱容器
#             var successMessage = document.getElementById('successMessage'); // 获取成功消息元素
#             successMessage.style.display = 'block'; // 显示成功消息
#         }
#     </script>
# </form>
#
# '<!-- /wp:html -->
# '''
# content3 = '''
# '<!-- wp:html -->
# <img src="alarm.png" alt="我的鬧鐘">
# <!-- /wp:html -->'
# '''
# # Header
# headers = {
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
#     "Authorization": "Basic {}".format(token.decode("utf-8")),
#     "content-type": "application/json",
# }
# file_path = 'alarm.png'
# # 創建一個多部分表單數據編碼器
# multipart_data = MultipartEncoder(
#     fields={
#         # HTML內容部分
#         'html_file': ('content.html', content3, 'text/html'),
#         # 圖片文件部分
#         'image_file': ('alarm.png', open(file_path, 'rb'), 'image/png')
#     }
# )
#
# post = {
#     "content": content3,
# }
#
# # Post
# r = requests.post(
#     "{}/{}".format(url, 2389),
#     data=multipart_data,
#     headers=headers,
#     json=post,
# )
#
# link = json.loads(r.text).get('link')
# print(f'link = {link}')
#
# pprint(r.text)

# content = get_post_content(2542)
# print(content)

with open('singer_info.json', 'r', encoding='utf-8') as f:
    singer_data = json.load(f)
with open('concert_4_15_1.json', 'r', encoding='utf-8') as f:
    concert_data = json.load(f)

# post_singer(data[506])
singer_add_concert(2560, concert_data[100])
