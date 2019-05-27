import http.client, urllib.parse, json, time
import flask
import requests

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('sA7NOs4hqtmLF/dcFXxo7XU75QDAJB7tH+7XizXyrEWssjeeECPT+uVj1ylcYtw4Az99heGKPrYiU9pTRkY2COLyl5b0UoXV7Bl+qS29R+CqmCAtjwkgL8RIwsKj40NbK+UVGewiHSVy3rpUYOCB8AdB04t89/1O/w1cDnyilFU=') #YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('fb7f861ad12ec1cbdf8e9711b7c7c7c5')#YOUR_CHANNEL_SECRET
count=0
error_count = 0

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
        #print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    intent = get_answer(event.message.text)
    if intent == "沒有熱水":
        mes="好的,XX先生, 我們一起來檢查一下您的使用環境,1.請確認您的瓦斯桶或天然氣瓦斯管道, 是否確定已經打開?並檢查瓦斯管沒有折到或被東西壓住。如果有此情況, 請把開關打開, 瓦斯管理順後, 再試一下是否正常?"
        line_bot_api.reply_message(
        		  event.reply_token,
        		  TextSendMessage(text=mes))
    if intent == "有瓦斯味":
        mes="我們先來DIY自主檢查下，看看是否能解決您的問題。確認沒有廢氣回流。避免一直重覆開開關關熱水;您可以參考這份檢查教學說明："+"https://buy.sakura.com.tw/files/3614.pdf"+"\n"+"若檢後查仍然有問題, 您可以輸入995」,將派專業服務人員到府上維修。"
        line_bot_api.reply_message(
        		  event.reply_token,
        		  TextSendMessage(text=mes))
    if intent == "水太燙":
        mes=" 我們先來DIY自主檢查下，看看是否能解決您的問題。確認溫度已調至最低。確認熱水龍頭省水閥，請取下。已清潔水龍頭濾網及蓮蓬頭內異物;您可以參考這份檢查教學說明："+"https://buy.sakura.com.tw/files/3614.pdf"+"\n"+"若檢後查仍然有問題, 您可以輸入995」,將派專業服務人員到府上維修。"
        line_bot_api.reply_message(
        		  event.reply_token,
        		  TextSendMessage(text=mes))
    if intent == "故障_未確認":
        mes="請問熱水器使用上遇到什麼問題呀?"
        line_bot_api.reply_message(
        		  event.reply_token,
        		  TextSendMessage(text=mes))
    if intent == "忽冷忽熱":
        mes="我們先來DIY自主檢查下，看看是否能解決您的問題。確認瓦斯開關已開啟。確認瓦斯管無彎折或壓到。溫度已調至最高;您可以參考這份檢查教學說明："+"https://buy.sakura.com.tw/files/3614.pdf"+"\n"+"若檢後查仍然有問題, 您可以輸入995」,將派專業服務人員到府上維修。"
        line_bot_api.reply_message(
        	      event.reply_token,
        		  TextSendMessage(text=mes))
    if intent == "叫人":
        mes="已經為您登記維修, 服務人員將於明日上午10點前致電給您，確認服務時間。感謝您使用AI客服小花~~"
        line_bot_api.reply_message(
                  event.reply_token,
                  TextSendMessage(text=mes))
    if intent == "已經排除":
        mes="太好了!很高興為您服務"
        line_bot_api.reply_message(
                  event.reply_token,
                  TextSendMessage(text=mes))
    if intent == "瓦斯問題未排除":
        mes="請檢查熱水器插座沒有鬆脫且正常供電,並檢查熱水水壓及水量是否正常?"
        line_bot_api.reply_message(
                  event.reply_token,
                  TextSendMessage(text=mes))
    if intent == "其他問題未排除":
        mes="唉呀, 看來需要派個專家過去幫您排除"
        line_bot_api.reply_message(
                  event.reply_token,
                  TextSendMessage(text=mes))
    if intent == 'None':
        mes = "真歹勢,小花沒有理解您的問題,能請您換個說法嗎?熱水器有什麼問題呀?"
        line_bot_api.reply_message(
                  event.reply_token,
                  TextSendMessage(text=mes))
        # if intent == 'None':
#         	error_count+=1
#         	line_bot_api.reply_message(
#         		event.reply_token,
#         		TextSendMessage(text='我們先來DIY自主檢查下...'))
        

def get_answer(message_text):
    
    params ={
    # Query parameter
    'q': message_text,
    # Optional request parameters, set to default values
    'timezoneOffset': '0',
    'verbose': 'false',
    #'spellCheck': 'false',
    #'staging': 'false',
    }
    url = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/84097858-9522-46c3-ad22-d536589e7672?verbose=true&timezoneOffset=-360&subscription-key=01f9fe93b2774c1ebef36f747289ca96'
    r = requests.get(url,params=params)
    #print('response from Luis in json format', r.json())
    Luis_Data = r.json()
    topintent = Luis_Data['topScoringIntent']['intent']
    print (topintent,Luis_Data['topScoringIntent']['score'])
    # if intent != 'None':
#     	count+=1
    return topintent
    

if __name__ == "__main__":
    app.run(port = 5000)

