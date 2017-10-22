import os, sys
from flask import Flask, request
from utils import wit_response, get_news_elements, handle_message

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'verify-token')

app = Flask(__name__)

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
    message_event = request.get_json()
    log(message_event)

    handle_message(message_event)

    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 8080)
