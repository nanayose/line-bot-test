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
    {
        "運勢": "🌟超大当たり",
        "えまみくじ": "神降臨",
        "ギャンブル運": "★★★★★★☆",
        "メッセージ": "あなたの背後に神が見えます。今すぐホールへ行きましょう。",
        "えまから一言": "もう当たる未来しか見えん。えまも出撃するわ。"
    },
    "🌟超大当たり：神降臨「あなたの背後に神が見えます。今すぐホールへ行きましょう。」",
    "🌟超大当たり：覇者の光「7揃いが見える…！何しても当たります。」",
    "🌟超大当たり：金色爆連神「大当たりの波が止まらない！取りきれないコース、確定演出。」",
    "💮大吉：一撃爆発吉「投資1k、回収∞。今日は笑って帰れる日。」",
    "💮大吉：フラッシュ吉「静かにしてろ…聞こえるだろあの音が。」",
    "💮大吉：神社帰り吉「お祓い完了。邪念が消えたらヒキが戻る。」",
    "💮大吉：ラッキー吉「隣の常連さんがコーヒーくれるレベルの幸運。」",
    "💮大吉：ホールの祝福吉「誰よりも早く初当たりを掴みし者。」",
    "🥈中吉：朝イチヒット吉「100回転以内に光が…！（たぶん）」",
    "🥈中吉：右肩上がり吉「投資はかさんでも、最後に帳尻が合うタイプ。」",
    "🥈中吉：奇跡の引き戻し吉「引き戻してドヤ顔していい日。」",
    "🥈中吉：プレミア勘違い吉「出た！……と思ったら通常演出でした。気をつけて」",
    "🥈中吉：まあまあ良き吉「負けても心が負けなければ勝ち。今日はそんな日。」",
    "🥉小吉：回らないけど当たる吉「回転数はダメでも運でカバーせよ。」",
    "🥉小吉：ごはん代セーフ吉「負けたけど、晩ごはんは贅沢していい日。」",
    "🥉小吉：一撃だけ吉「ワンチャンある。それを信じるかはあなた次第。」",
    "🥉小吉：たぶん勝ち越し吉「たぶんプラス。でも計算したくないやつ。」",
    "🥉小吉：臨時出費吉「勝った金額、突然の出費で消えそうです。だから勝っておこうね」",
    "📈吉：飲まれきる前に当たる吉「運命はギリギリで動く。諦めるな」",
    "📈吉：微笑み神吉「演出が可愛い日。勝てるかは別。台を楽しもうよ」",
    "📈吉：気分だけ吉「勝ってる気がする。実際はチャラくらい。」",
    "📈吉：財布の中は据え置き吉「投資も回収も同じくらい。打ちたくなるヤツ。」",
    "📈吉：ゾーンすり抜け吉「チャンスゾーン？スルーして通常戻り。」",
    "📉末吉：最終回転吉「最後の保留で当たる…ような気がする日。」",
    "📉末吉：ハズレ吉「期待した演出が速攻で終わる日。」",
    "📉末吉：演出過多吉「激アツがたくさん出るけど、全部ハズレます。」",
    "📉末吉：当たり行方不明吉「当たりが来そうで来ないモヤモヤ日。」",
    "📉末吉：耐久吉「そろそろ当たってもええやろ…と100回思う。」",
    "⚠️凶：心が折れる凶「二度とあのホールに行かないと誓う日。」",
    "⚠️凶：初当たり単発凶「単発地獄の開幕だッ！」",
    "⚠️凶：投資嵩み凶「今日の千円は10秒で消えます。」",
    "⚠️凶：隣だけ連チャン凶「隣が当たるたび、心が死ぬ日。」",
    "⚠️凶：やめたら当たる凶「自分がやめた台がその後爆連します。」",
    "💀大凶：札消失大凶「財布の中がスッカラカンになります。」",
    "💀大凶：リーチも来ない大凶「“通常時”ですらない静けさ。」",
    "💀大凶：帰りに転ぶ大凶「負けた上に物理的にも痛い目に遭う日。」",
    "🌀変吉「よくわからんけど、勝った。そんな奇跡が起きるかも。」",
    "😈えまの呪い：深追いの呪い「あと1回…が、あと10回転…が、帰れなくなる呪い。」",
    "😈えまの呪い：見せ場ゼロの呪い「誰にも話せない…何もなかった日の記憶。」",
    "🌕裏・大吉：神域の哲学「勝ちとは幻想、ホールは試練、人生はヒキ強の運ゲー。」",
    "🦊えま吉：巫女覚醒えま吉「今日は私が台を祝福した。…たぶん当たるで。」",
    "🦊えま吉：七寄流・逆張り吉「今日打ったら負ける。だから打て（？）」"
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
        reply_text = (
            f"運勢　: {result['運勢']}\n"
            f"えまみくじ　: {result['えまみくじ']}\n"
            f"ギャンブル運　: {result['ギャンブル運']}\n"
            f"メッセージ　: {result['メッセージ']}\n"
            f"えまから一言　: {result['えまから一言']}"
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「おみくじ」と送ってくれたら運勢を占うよ！")
        )

if __name__ == "__main__":
    app.run()
