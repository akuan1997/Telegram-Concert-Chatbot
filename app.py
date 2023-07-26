import os
import sys
import mysql.connector

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'mT37wrputZJwRjvsqmRCI9WHF2VvSZITKRI9PnrtB9FK/tNa0fvN2YHWWIpJyecemA4wII59L8Y5mfWZBDsy0RR+8qRhoaj0i2cK54wIhTxWLhh0Hw6tH6U82hRtKuWkDQA/MMaDqn46Z3XvgIkYTQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('3dffbf1fbe8965a51036b07387925f61')


# line_bot_api.push_message('@174keasc', TextSendMessage(text='你可以開始了'))

def log(message):
    print(message)
    sys.stdout.flush()


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


# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    cnx = mysql.connector.connect(
        host='192.168.56.1',
        user='remote_user',
        passwd='fjfj',
        database='prc1'
    )
    cursor = cnx.cursor()

    cursor.execute('SELECT * FROM Concerts')
    for x in cursor:
        print(x)
        log(x)