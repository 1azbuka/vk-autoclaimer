import requests
from time import localtime, strftime

webhook = ''

def embed(title, description, color):
    data = requests.post(webhook, json={
        'embeds': [
            {
                'title': title,
                'description': description,
                'footer': {
                    'text': f'The report was generated on {strftime("%Y-%m-%d %H:%M:%S", localtime())}'
                },
                'color': color
            }
        ]
    })
    return data

def message(content):
    data = requests.post(webhook, json={
        'content': content
    })
    return data