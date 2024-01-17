from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'vJMIfP2jAsI/ObLRFNZa7PIqpxaNcuq0aQw7FercJbkpkvPDDasD6g+zWZUb+Z6nVorbqjXji5RocmsngiTXjY8J4RynAQMgvvG9Hw3shnrm0/UiI1ayS9fsNa09SHiYfPvN5rSX0lDpVURE4LXJMAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('68c1b8695588cee25d5abe0ed0ee12cd')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('123',message):
        carousel_template_message = TemplateSendMessage(
            alt_text='免費教學影片123123123123123123123',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        # thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
                        title='Python基礎教學',
                        text='萬丈高樓平地起',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=270'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
                        title='Line Bot聊天機器人',
                        text='台灣最廣泛使用的通訊軟體',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='Line Bot申請與串接'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=2532'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
                        title='Telegram Bot聊天機器人',
                        text='唯有真正的方便，能帶來意想不到的價值',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='Telegrame申請與串接'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=2648'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)