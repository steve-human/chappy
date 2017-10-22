import os
from wit import Wit
from gnewsclient import gnewsclient
from pymessenger import Bot

WIT_ACCESS_TOKEN = os.getenv('WIT_ACCESS_TOKEN', 'wit-access-token')
PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN', 'fb-page-access-token')

client = Wit(access_token = WIT_ACCESS_TOKEN)
bot = Bot(PAGE_ACCESS_TOKEN)

def wit_response(message_text):
    response = client.message(message_text)
    categories = {'newstype':None, 'location':None}

    entities = list(response['entities'])
    for entity in entities:
        categories[entity] = response['entities'][entity][0]['value']

    return categories

def get_news_elements(categories):
    news_client = gnewsclient()
    news_client.query = ''

    if categories['newstype'] != None:
        news_client.query += categories['newstype'] + ' '

    if categories['location'] != None:
        news_client.query += categories['location']

    news_items = news_client.get_news()

    elements = []

    for item in news_items:
        element = {
            'title': item['title'],
            'buttons': [{
                'type': 'web_url',
                'title': 'Read more',
                'url': item['link']
            }],
            'image_url': item['img']
        }
        elements.append(element)

    return elements

def handle_message(message):
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
                        bot.send_text_message(sender_id, "Sure do! Here you go...")
                        elements = get_news_elements(categories)
                        bot.send_generic_message(sender_id, elements)
