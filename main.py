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
        "ラッキーアイテム": "キーホルダー",
        "メッセージ": "あなたの背後に神が見えます。今すぐホールへ行きましょう。",
        "えまから一言": "もう当たる未来しか見えん。えまも出撃するわ。"
    },
    {
        "運勢": "🌟超大当たり",
        "えまみくじ": "覇者の光",
        "ギャンブル運": "★★★★★★☆",
        "ラッキーアイテム": "コンビニの新作",
        "メッセージ": "7揃いが見える…！何しても当たります。",
        "えまから一言": "止まらない勝利の波！財布のヒモはゆるめてええで！"
    },
    {
        "運勢": "🌟超大当たり",
        "えまみくじ": "金色爆連神",
        "ギャンブル運": "★★★★★★☆",
        "ラッキーアイテム": "旧札",
        "メッセージ": "大当たりの波が止まらない！取りきれないコース、確定演出。",
        "えまから一言": "爆連注意報発令中！今日は全力で楽しんでな！"
    },
    {
        "運勢": "💮大吉",
        "えまみくじ": "一撃爆発吉",
        "ギャンブル運": "★★★★★☆☆",
        "ラッキーアイテム": "手洗いうがい",
        "メッセージ": "投資1k、回収∞。今日は笑って帰れる日。",
        "えまから一言": "一撃必殺の強運、今日のアナタは神がかっとるで！"
    },
{
        "運勢": "💮大吉",
        "えまみくじ": "フラッシュ吉",
        "ギャンブル運": "★★★★★☆☆",
        "ラッキーアイテム": "新しい靴下",
        "メッセージ": "静かにしてろ…聞こえるだろあの音が。",
        "えまから一言": "静寂の中の大チャンス、耳澄ませといてな！"
    },
    {
        "運勢": "💮大吉",
        "えまみくじ": "神社帰り吉",
        "ギャンブル運": "★★★★★☆☆",
        "ラッキーアイテム": "炭酸ドリンク",
        "メッセージ": "お祓い完了。邪念が消えたらヒキが戻る。",
        "えまから一言": "お祓いパワー炸裂！新しい運気をつかむんやで！"
    },
     {
        "運勢": "💮大吉",
        "えまみくじ": "ラッキー吉",
        "ギャンブル運": "★★★★★☆☆",
        "ラッキーアイテム": "イヤホン",
        "メッセージ": "隣の常連さんがコーヒーくれるレベルの幸運。",
        "えまから一言": "隣の人も味方！小さなラッキーに感謝しようや♪"
    },
     {
        "運勢": "💮大吉",
        "えまみくじ": "ホールの祝福吉",
        "ギャンブル運": "★★★★★☆☆",
        "ラッキーアイテム": "飴",
        "メッセージ": "誰よりも早く初当たりを掴みし者。",
        "えまから一言": "最速のヒキを持つアナタ、今日も快調やな！"
    },
     {
        "運勢": "🥈中吉",
        "えまみくじ": "朝イチヒット吉",
        "ギャンブル運": "★★★★☆☆☆",
        "ラッキーアイテム": "買ったことないお菓子",
        "メッセージ": "100回転以内に光が…！（たぶん）",
        "えまから一言": "早めのヒット狙い、期待して待っとこ！"
    },
    {
        "運勢": "🥈中吉",
        "えまみくじ": "右肩上がり吉",
        "ギャンブル運": "★★★★☆☆☆",
        "ラッキーアイテム": "マスク",
        "メッセージ": "投資はかさんでも、最後に帳尻が合うタイプ。",
        "えまから一言": "粘りが勝負の鍵、最後まで諦めんなよ！"
    },
    {
        "運勢": "🥈中吉",
        "えまみくじ": "奇跡の引き戻し吉",
        "ギャンブル運": "★★★★☆☆☆",
        "ラッキーアイテム": "赤いもの",
        "メッセージ": "引き戻してドヤ顔していい日。",
        "えまから一言": "引き戻しパワー全開！自信満々で行くぞ！"
    },
    {
        "運勢": "🥈中吉",
        "えまみくじ": "プレミア勘違い吉",
        "ギャンブル運": "★★★★☆☆☆",
        "ラッキーアイテム": "アクセサリー",
        "メッセージ": "出た！……と思ったら通常演出でした。気をつけて",
        "えまから一言": "油断大敵！騙されてもめげない心が強運を呼ぶ！"
    },
    {
        "運勢": "🥈中吉",
        "えまみくじ": "当たると思えば当たる吉",
        "ギャンブル運": "★★★★☆☆☆",
        "ラッキーアイテム": "ラーメン",
        "メッセージ": "挙動はダメでも運でカバーせよ。",
        "えまから一言": "運命の一撃が待ってる！諦めんといて！"
    },
     {
        "運勢": "🥉小吉",
        "えまみくじ": "まあまあ良き吉",
        "ギャンブル運": "★★★☆☆☆☆",
        "ラッキーアイテム": "カレンダー",
        "メッセージ": "負けても心が負けなければ勝ち。今日はそんな日。",
        "えまから一言": "結果よりも気持ちが大事。前向きに行こうや！"
    },
    {
        "運勢": "🥉小吉",
        "えまみくじ": "ごはんもりもり吉",
        "ギャンブル運": "★★★☆☆☆☆",
        "ラッキーアイテム": "肉",
        "メッセージ": "負けたけど、晩ごはんは贅沢していい日。",
        "えまから一言": "プラスは無理でも、気持ちはリッチにな♪"
    },
     {
        "運勢": "🥉小吉",
        "えまみくじ": "一撃だけ吉",
        "ギャンブル運": "★★★☆☆☆☆",
        "ラッキーアイテム": "自販機",
        "メッセージ": "ワンチャンある。それを信じるかはあなた次第。",
        "えまから一言": "信じる者は救われる！好機、期待してみてな！"
    },
     {
        "運勢": "🥉小吉",
        "えまみくじ": "たぶん勝ち越し吉",
        "ギャンブル運": "★★★☆☆☆☆",
        "ラッキーアイテム": "ガチャガチャ",
        "メッセージ": "たぶんプラス。でも計算したくないやつ。",
        "えまから一言": "細かいことは気にせーへん！勝利の女神は微笑む！"
    },
     {
        "運勢": "🥉小吉",
        "えまみくじ": "臨時出費吉",
        "ギャンブル運": "★★★☆☆☆☆",
        "ラッキーアイテム": "時計",
        "メッセージ": "勝った金額、突然の出費で消えそうです。だから勝っておこうね",
        "えまから一言": "気は抜かれへん！でも笑顔で乗り切ろうや！"
    },
    {
        "運勢": "📈吉",
        "えまみくじ": "飲まれきる前に当たる吉",
        "ギャンブル運": "★★☆☆☆☆☆",
        "ラッキーアイテム": "グミ",
        "メッセージ": "運命はギリギリで動く。諦めるな",
        "えまから一言": "諦めたら終わり！最後までチャンスはあるで！"
    },
   {
        "運勢": "📈吉",
        "えまみくじ": "微笑み神吉",
        "ギャンブル運": "★★☆☆☆☆☆",
        "ラッキーアイテム": "音量3",
        "メッセージ": "演出が可愛い日。勝てるか3別。まぁ今日くらい台を楽しもうよ",
        "えまから一言": "楽しむ心が一番のヒキを呼ぶんや！"
    },
    {
        "運勢": "📈吉",
        "えまみくじ": "追い厳禁吉",
        "ギャンブル運": "★★☆☆☆☆☆",
        "ラッキーアイテム": "パン",
        "メッセージ": "今日はもう一回が命取り。引き際が肝心",
        "えまから一言": "今日は勝ち逃げの才能が試されてんちゃうか！？"
    },
    {
        "運勢": "📈吉",
        "えまみくじ": "財布の中は据え置き吉",
        "ギャンブル運": "★★☆☆☆☆☆",
        "ラッキーアイテム": "LINE",
        "メッセージ": "投資も回収も同じくらい。打ちたくなるヤツ。",
        "えまから一言": "波に乗れるかはアナタ次第。焦らず行こうや！"
    },
    {
        "運勢": "📈吉",
        "えまみくじ": "ゾーンすり抜け吉",
        "ギャンブル運": "★★☆☆☆☆☆",
        "ラッキーアイテム": "休みの予定をたてる",
        "メッセージ": "CZスルー。",
        "えまから一言": "チャンスは見逃すな！次に期待しようや！"
    },
    {
        "運勢": "📉末吉",
        "えまみくじ": "最終回転吉",
        "ギャンブル運": "★☆☆☆☆☆☆",
        "ラッキーアイテム": "ペン",
        "メッセージ": "最後の保留で当たる…ような気がする日。",
        "えまから一言": "最後まで諦めない心が未来を変えるんや！"
    },
    {
        "運勢": "📉末吉",
        "えまみくじ": "ハズレ吉",
        "ギャンブル運": "★☆☆☆☆☆☆",
        "ラッキーアイテム": "おにぎり",
        "メッセージ": "期待した演出が速攻で終わる日。",
        "えまから一言": "悔しいけど、次はきっと良くなるで！"
    },
    {
        "運勢": "📉末吉",
        "えまみくじ": "演出過多吉",
        "ギャンブル運": "★☆☆☆☆☆☆",
        "ラッキーアイテム": "Tシャツ",
        "メッセージ": "激アツがたくさん出るけど、全部ハズレます。",
        "えまから一言": "騙されても気にせーへん！それも運命！"
    },
    {
        "運勢": "📉末吉",
        "えまみくじ": "当たり行方不明吉",
        "ギャンブル運": "★☆☆☆☆☆☆",
        "ラッキーアイテム": "塩",
        "メッセージ": "当たりが来そうで来ないモヤモヤ日。",
        "えまから一言": "焦らずじっと我慢。チャンスはまた来る！"
    },
    {
        "運勢": "📉末吉",
        "えまみくじ": "耐久吉",
        "ギャンブル運": "★☆☆☆☆☆☆",
        "ラッキーアイテム": "新しい歯ブラシ",
        "メッセージ": "そろそろ当たってもええやろ…と100回思う。",
        "えまから一言": "忍耐力が試される日。根気強くな！"
    },
    {
        "運勢": "⚠️凶",
        "えまみくじ": "心が折れる凶",
        "ギャンブル運": "☠",
        "ラッキーアイテム": "薬局",
        "メッセージ": "二度とあのホールに行かないと誓う日",
        "えまから一言": "心は折れても諦めんな。次はきっと勝てるぞ！"
    },
    {
        "運勢": "⚠️凶",
        "えまみくじ": "初当たり単発凶",
        "ギャンブル運": "☠",
        "ラッキーアイテム": "アニメ",
        "メッセージ": "単発地獄の開幕だッ！",
        "えまから一言": "おそらく今日は勝てん！"
    },
    {
        "運勢": "⚠️凶",
        "えまみくじ": "投資嵩み凶",
        "ギャンブル運": "☠☠",
        "ラッキーアイテム": "たこ焼き",
        "メッセージ": "今日の千円は10秒で消えます。",
        "えまから一言": "財布が悲鳴をあげる前にストップ！"
    },
    {
        "運勢": "⚠️凶",
        "えまみくじ": "隣だけ連チャン凶",
        "ギャンブル運": "☠☠",
        "ラッキーアイテム": "朝日の写真",
        "メッセージ": "隣が当たるたび、心が死ぬ日。",
        "えまから一言": "隣は隣…大丈夫…"
    },
  {
        "運勢": "⚠️凶",
        "えまみくじ": "やめたら当たる凶",
        "ギャンブル運": "☠☠☠",
        "ラッキーアイテム": "新しい歯ブラシ",
        "メッセージ": "自分がやめた台がその後爆連します。",
        "えまから一言": "続けるも地獄、やめるも地獄…"
    },
    {
        "運勢": "💀大凶",
        "えまみくじ": "札消失大凶",
        "ギャンブル運": "☠☠☠☠☠",
        "ラッキーアイテム": "酒",
        "メッセージ": "財布の中がスッカラカンになります。",
        "えまから一言": "財布は守ろう。今日は休む日かもな…"
    },
    {
        "運勢": "💀大凶",
        "えまみくじ": "リーチも来ない大凶",
        "ギャンブル運": "☠☠☠☠☠",
        "ラッキーアイテム": "昼寝",
        "メッセージ": "通常時”ですらない静けさ。",
        "えまから一言": "静かな時間も大事ということか…"
    },
    {
        "運勢": "💀大凶",
        "えまみくじ": "帰りに転ぶ大凶",
        "ギャンブル運": "☠☠☠☠☠",
        "ラッキーアイテム": "旧500円玉",
        "メッセージ": "負けた上に物理的にも痛い目に遭う日。",
        "えまから一言": "今日は家からは出るな！明日がある！"
    },
   {
        "運勢": "？？？",
        "えまみくじ": "🌀変吉",
        "ギャンブル運": "★★★★☆☆☆",
        "ラッキーアイテム": "家電",
        "メッセージ": "よくわからんけど、勝った。そんな奇跡が起きるかも。",
        "えまから一言": "今日の運は未知数！レッツGO！"
    },
    {
        "運勢": "？？？",
        "えまみくじ": "見せ場ゼロ吉",
        "ギャンブル運": "★☆☆☆☆☆☆",
        "ラッキーアイテム": "買い物",
        "メッセージ": "誰にも話せない…何もなかった日の記憶。",
        "えまから一言": "無事に終わるのもヒキのうち。お疲れ様！"
    },
    {
        "運勢": "🌕裏・大吉",
        "えまみくじ": "神域の哲学吉",
        "ギャンブル運": "★★★★★★☆",
        "ラッキーアイテム": "和菓子",
        "メッセージ": "勝ちとは幻想、ホールは試練、人生はヒキ強の運ゲー。",
        "えまから一言": "真理を知る者よ。今日も運を味方につけようや！"
    },
    {
        "運勢": "🦊えま吉",
        "えまみくじ": "巫女覚醒えま吉",
        "ギャンブル運": "★★★★★★☆",
        "ラッキーアイテム": "外食",
        "メッセージ": "今日は私が台を祝福した。…たぶん当たるで。",
        "えまから一言": "巫女パワー全開！信じて突っ込め〜！負けて文句言ったら呪うで"
    },
   {
        "運勢": "🦊えま吉",
        "えまみくじ": "七寄流・逆張り吉",
        "ギャンブル運": "★★★★★★☆",
        "ラッキーアイテム": "外食",
        "メッセージ": "今日打ったら負ける。だから打て（？）",
        "えまから一言": "逆張りの極意伝授。オカルトが吉！"
    },
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
            f"ラッキーアイテム　: {result['ラッキーアイテム']}\n"
            f"メッセージ　: {result['メッセージ']}\n"
            f"えまから一言　: {result['えまから一言']}"
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

    elif any(word in user_message for word in ["負け", "まけ", "死んだ", "終わった", "負けた", "まけた"]):
        messages = [
            "今日はたまたま運が悪かっただけ…次はきっと勝てるで！",
            "負けても大丈夫！私はあなたの味方やで。",
            "そんな日もあるさ！ギャンブルはメンタルスポーツ！",
            "一緒に泣こ…でも次は笑えるように応援するで！",
            "よし、次は勝ちフラグ立てにいこっか！"
        ]
        reply_message = random.choice(messages)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="えまから慰めの一言：\n" + reply_message)
        )

    elif any(word in user_message for word in ["勝ち", "かち", "勝った", "出た", "爆連"]):
        congrats = [
            "やったな！ほな焼肉や！",
            "勝利おめでとう🎉 私も嬉しい！",
            "その調子で明日も勝ち確やで！",
            "出玉モリモリおめ！今日はご褒美や！",
            "さすがやな、ヒキ強の神や！"
        ]
        reply_message = random.choice(congrats)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="えまからお祝いの一言：\n" + reply_message)
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「おみくじ」と送ってくれたら運勢を占うよ！")
        )
        
if __name__ == "__main__":
    app.run()
