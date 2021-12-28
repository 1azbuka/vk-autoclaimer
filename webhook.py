from time import localtime, strftime
import requests
import yaml

config = yaml.safe_load(open('config.yml', 'r').read())

def embed(title, description, color):
    data = requests.post(config['webhook'], json={
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
    data = requests.post(config['webhook'], json={
        'content': content
    })
    return data
