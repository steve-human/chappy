import os
from wit import Wit
from gnewsclient import gnewsclient

WIT_ACCESS_TOKEN = os.getenv('WIT_ACCESS_TOKEN', 'wit-access-token')

client = Wit(access_token = WIT_ACCESS_TOKEN)

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

resp = wit_response("thanks")

if resp['thanks']:
    print('Your welcome')
else:
    print('How rude!')
