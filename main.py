from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random

# LINEチャネルのアクセストークンとシークレット
LINE_CHANNEL_ACCESS_TOKEN = 'N03d1q0yIxPseCAespxFFY4OQx1TuvjKYGZdxI0KrUxMLyPrntHTFDPSxw+ndRTehSFdfhFnGbUloX4SF+4/GK1uaimcCS07w5fjfJRYcPWX2klBeKOPbDWjsX3wsiFjQeNP2clkGs2ih1ZvxKgZwQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '9ce50b138f2ae48cdfe09adedf17126f'

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# おみくじ一覧
omikuji_list = [
    "🌟超大当たり：神降臨「あなたの背後に神が見えます。今すぐホールへ行きましょう。」",
    "🌟超大当たり：覇者の光「7揃いが見える…！何しても当たります。」",
    "🌟超大当たり：金色爆連神「大当たりの波が止まらない！取りきれないコース、確定演出。」",
    "💮大吉：一撃爆発吉「投資1k、回収∞。今日は笑って帰れる日。」",
    # 省略してるだけで、ヒロト様のリストそのまま貼ってOK
    "🦊えま吉：七寄流・逆張り吉「今日打ったら負ける。だから打て（？）」
]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message == "おみくじ":
        result = random.choice(omikuji_list)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「おみくじ」と送ってくれたら運勢を占うよ！")
        )

if __name__ == "__main__":
    app.run()
