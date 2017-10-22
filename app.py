import os, sys
from flask import Flask, request
from utils import wit_response, get_news_elements
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN', 'fb-page-access-token')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'verify-token')

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                #IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    categories = wit_response(messaging_text)

                    if 'thanks' in categories and categories['thanks'] == 'true':
                        bot.send_text_message(sender_id, "You're welcome!")
                    elif 'greetings' in categories and categories['greetings'] == 'true':
                        bot.send_text_message(sender_id, "Hey, what's new?")
                    else:
                        elements = get_news_elements(categories)
                        bot.send_generic_message(sender_id, elements)

    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 8080)
