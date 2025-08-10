from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import json

app = Flask(__name__)

# 環境変数からLINEのアクセストークンとシークレット取得
LINE_CHANNEL_ACCESS_TOKEN = 'N03d1q0yIxPseCAespxFFY4OQx1TuvjKYGZdxI0KrUxMLyPrntHTFDPSxw+ndRTehSFdfhFnGbUloX4SF+4/GK1uaimcCS07w5fjfJRYcPWX2klBeKOPbDWjsX3wsiFjQeNP2clkGs2ih1ZvxKgZwQdB04t89/1O/w1cDnyilFU='

LINE_CHANNEL_SECRET = '9ce50b138f2ae48cdfe09adedf17126f'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# おみくじデータ
OMIKUJI_RESULT = {
    "運勢": "🌟超大当たり",
    "えまみくじ": "神降臨",
    "星評価": "★★★★★★☆",  # 同じキー名は使えないからここは別名に
    "ラッキーアイテム": "キーホルダー",
    "メッセージ": "今日のあなたは無敵モード！何をしても追い風が吹く日。大胆に動けば運命が味方します！",
    "えまから一言": "神、降りちゃったね。今日のあなたはもう…七寄えま認定“幸運の申し子”です！"
}

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
    # おみくじ結果を整形して送信
    result_text = "\n".join([f"{key} : {value}" for key, value in OMIKUJI_RESULT.items()])
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result_text)
    )

if __name__ == "__main__":
    app.run(port=5000)
