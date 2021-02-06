try:
    import unzip_requirements
except ImportError:
    pass
import boto3
import json
import logging

from slack import notify_slack
from twitter import notify_twitter


logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.resource('sqs')
QUEUE_NAME = 'finapp'
queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)


def handle_sqs_message(event, context):
    logger.info(json.dumps(event))
    # msgs = queue.receive_messages()
    msgs = event['Records']
    for msg in msgs:
        msg_json = json.loads(msg['body'].strip("'<>() ").replace('\'', '\"'))
        if msg_json['target'] == 'slack':
            notify_slack(
                msg=msg_json['message'],
                channel=msg_json['channel']
            )
        elif msg_json['target'] == 'twitter':
            notify_twitter(
                msg=msg_json['message'],
            )
