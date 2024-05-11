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
    print(f"成功刪除post_id為{post_id}的文章")
    # pprint(r.text)


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
    latter = new_concert + content.split('<h1>即將來臨的演唱會</h1>')[1] + "<!-- /wp:html -->"
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
        print('成功寫入concert_pin_postid.txt')

    # Print
    # pprint(r.text)
    print(f"成功新增演唱會文章 {data['tit']}")


# with open('singer_info.json', 'r', encoding='utf-8') as f:
#     singer_data = json.load(f)
# with open('concert_4_15_1.json', 'r', encoding='utf-8') as f:
#     concert_data = json.load(f)
#
# # post_singer(data[506])
# singer_add_concert(2560, concert_data[100])
def update_post_content(post_id, data):
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
        "{}/{}".format(url, post_id),
        headers=headers,
        json=post,
    )

    print(f"文章編號{post_id}修改成功")


def testing_add_concert():
    with open('test1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i in range(len(data)):
        post_concert(data[i])

# testing_add_concert()

# # Post info
# post = {
#     "title": '測試1',
#     "content": '測試2',
#     "status": "publish"
# }
#
# # Post
# r = requests.post(
#     url,
#     headers=headers,
#     json=post,
# )
#
# # Print
# pprint(r.text)

# data = read_json("singer_info.json")
# for i in range(1, len(data)):
#     post_singer(data[i])
