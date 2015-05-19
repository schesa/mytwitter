import pika
import json

from mytwitter import constants
from mytwitter.db import api as db_api
from mytwitter.db import models


class MyTwitterServerRPCAPI(object):
    def __init__(self):
        self._conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=constants.rpc_url))
        self._channel = self._conn.channel()
        self._channel.basic_qos(prefetch_count=1)
        self._channel.queue_declare(queue='mytwitter.rpc_queue')
        self._channel.basic_consume(self._on_request,
                                    queue='mytwitter.rpc_queue')

    def _on_request(self, ch, method, props, body):
        req = json.loads(body)
        print 'Got request: %s' % req

        response = {}
        func_name = req['func_name']
        args = req['args']
        kwargs = req['kwargs']

        try:
            func = getattr(db_api, func_name)
            response['ret_val'] = func(*args, **kwargs)
        except Exception as exc:
            response['err_message'] = exc.message
        print 'Sending back response: %s' % response

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                            correlation_id = props.correlation_id),
                         body=json.dumps(response,
                                         default=models.ModelJsonEncoder))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def accept(self):
        self._channel.start_consuming()
