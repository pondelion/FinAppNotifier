import os
import requests, json


try:
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
except:
    print('environment variable [SLACK_WEBHOOK_URL] is not set.')


def notify_slack(msg: str, channel: str):
    print(f'slack : {channel} : {msg}')
    payload = {
        'channel': f'#{channel}',
        'text': msg,
        'username': 'finapp_bot',
        'icon_emoji': ':ghost:'
    }
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
