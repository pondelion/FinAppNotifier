from enum import Enum


class SQSQueueName(Enum):

    TEST = 'finapp_test'
    PREDICTION_RESULT = 'finapp_prediction_result'
    STOP_LOW_HIGH = 'finapp_stop_low_high'


class SQSPolling:

    def __init__(
        self,
        boto_sqs_clint,
    ):
        self._sqs_clint = boto_sqs_clint

    def push_message(
        self,
        queue_name: SQSQueueName,
        message: str,
        group: str,
    ):
        queue_url = self._sqs_clint.get_queue_url(QueueName=queue_name.value)
        res = self._sqs_clint.send_message(
            QueueUrl=queue_url["QueueUrl"],
            MessageBody=message,
            MessageGroupId=group
        )
        return res
