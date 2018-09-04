from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'Charlie', # ชื่อแชตบ็อต
    read_only=True, # อ่านอย่างเดียว
    storage_adapter='chatterbot.storage.SQLStorageAdapter', # กำหนดการจัดเก็บ ในที่นี้เลือก chatterbot.storage.SQLStorageAdapter เก็บเป็น Sqllite
    logic_adapters=[
        {
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.TimeLogicAdapter",
            "chatterbot.logic.BestMatch"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        }
        
    ],
    database='Charlie.sqlite3' # ที่ตั้งฐานข้อมูล  
)

app = Flask(__name__)

line_bot_api = LineBotApi('HZhaPZ2OlTbKFxWvIcvPbdBfHP8aO6S7WCHeTCx4oHArhcfYLVmDBRN7PFkY1VlQDuJkswv+VjVfq/+GiZr/eZH6HXwsiVs407TiVIX/oqURw9klC9grqg49zzptrJ3+Iknq3CvkcIIPc06cijDjggdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('daef736e81f15e1f483debb7d4480727')

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/about')
def about():
    return 'The about page'

@app.route("/", methods=['POST'])
def webhook():
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response = chatbot.get_response(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(response)))


if __name__ == "__main__":
    app.run()

