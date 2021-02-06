from enum import Enum
from typing import Dict, Union
from dataclasses import dataclass
import json


class SQSQueueName(Enum):
    DEFAULT = 'finapp'


class Target(Enum):
    SLACK = 'slack'
    TWITTER = 'twitter'


@dataclass
class SlackMessage:
    target: Target = Target.SLACK
    channel: str
    message: str
    group_id: str
    media_url: str = None

    def to_json(self):
        data = {
            'target': self.target.value,
            'channel': self.channel,
            'message': self.message,
        }
        if self.media_url is not None:
            data['media_url'] = self.media_url
        return data


@dataclass
class TwitterMessage:
    target: Target = Target.TWITTER
    message: str
    group_id: str
    media_url: str = None

    def to_json(self):
        data = {
            'target': self.target.value,
            'message': self.message,
        }
        if self.media_url is not None:
            data['media_url'] = self.media_url
        return data


class SQSPolling:

    def __init__(
        self,
        boto_sqs_clint,
    ):
        self._sqs_clint = boto_sqs_clint

    def push_message(
        self,
        message: Union[SlackMessage, TwitterMessage],
        queue_name: SQSQueueName = SQSQueueName.DEFAULT,
    ):
        queue_url = self._sqs_clint.get_queue_url(QueueName=queue_name.value)
        msg_json = message.to_json()
        res = self._sqs_clint.send_message(
            QueueUrl=queue_url["QueueUrl"],
            MessageBody=json.dumps(msg_json),
            MessageGroupId=message.group_id
        )
        return res
