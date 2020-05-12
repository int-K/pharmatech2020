from flask import Flask, request, abort
import os
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "おめでとう！！"

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

@app.route("/push_test")
def push_test():
    
    carousel_template = CarouselTemplate(columns=[
               CarouselColumn(text='忘れずに服用できていますか？', title='服薬状況', actions=[
    #                    URIAction(label='Go to line.me', uri='https://line.me'),
                   PostbackAction(label='はい', data='はい', text='はい'),
                   PostbackAction(label='いいえ', data='いいえ', text='いいえ')
               ]),
               CarouselColumn(text='副作用と疑われる症状は出ていませんか？', title='副作用について', actions=[
                   PostbackAction(label='はい、出ていません',data='はい、出ていません', text='はい、出ていません'),
                   PostbackAction(label='いいえ、出ています', data='いいえ、出ています', text='いいえ、出ています')

               ]),
           ])
    template_message = TemplateSendMessage(alt_text='Confirm alt text', template=carousel_template)
    line_bot_api.broadcast(TemplateSendMessage(alt_text='服薬状況の確認', template=carousel_template))
    return "have sent"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == 'confirm':
        carousel_template = CarouselTemplate(columns=[
               CarouselColumn(text='忘れずに服用できていますか？', title='服薬状況', actions=[
    #                    URIAction(label='Go to line.me', uri='https://line.me'),
                   PostbackAction(label='はい', data='はい', text='はい'),
                   PostbackAction(label='いいえ', data='いいえ', text='いいえ')
               ]),
               CarouselColumn(text='副作用と疑われる症状は出ていませんか？', title='副作用について', actions=[
                   PostbackAction(label='はい、出ていません',data='はい、出ていません', text='はい、出ていません'),
                   PostbackAction(label='いいえ、出ています', data='いいえ、出ています', text='いいえ、出ています')

               ]),
           ])
        template_message = TemplateSendMessage(
               alt_text='Confirm alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif text == 'confirm2':
        confirm_template = ConfirmTemplate(text='病状はいかがですか?', actions=[
            PostbackAction(label='軽快している', data='軽快している', text='軽快している'),
            PostbackAction(label='改善してない', data='改善してない', text='改善してない')])
        template_message = TemplateSendMessage(
           alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif text == 'confirm3':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
           MessageAction(label='Yes', text='Yes!'),
           MessageAction(label='No', text='No!'),])
        template_message = TemplateSendMessage(alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
            
            
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'いいえ':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='服用方法が不明な場合は、薬剤師にご連絡してください'))
    elif event.postback.data == 'いいえ、出ています':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='副作用の有無について、薬剤師にご連絡してください'))
    elif event.postback.data == '改善してない':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='薬剤師にその旨をご連絡してください'))
    elif event.postback.data == 'はい':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='その調子！'))
    elif event.postback.data == '軽快している':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='その調子！いい感じです！'))
    elif event.postback.data == 'はい、出ていません':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='その調子！'))
        
        
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)