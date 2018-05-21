import json
import logging
import pika
import uuid

import mytwitter.config
from mytwitter import log

CONF = mytwitter.config.CONF
LOG = log.get_logger()


class MyTwitterClientRPCAPI(object):
    def __init__(self):
        creds = pika.PlainCredentials(CONF.amqp.user,
                                      CONF.amqp.password)
        self._conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=CONF.amqp.url,
                                      port=int(CONF.amqp.port),
                                      virtual_host=CONF.amqp.vhost,
                                      credentials=creds))
        self._channel = self._conn.channel()

    def call(self, func, *args, **kwargs):
        invoker = MyTwitterRPCInvoker(self._conn, self._channel)
        return invoker.call(func, *args, **kwargs)


class MyTwitterRPCInvoker(object):
    def __init__(self, conn, channel):
        self._conn = conn
        self._channel = channel
        result = self._channel.queue_declare(exclusive=True)
        self._callback_queue = result.method.queue

        self._channel.queue_declare(queue='mytwitter.amqp.queue')
        self._channel.basic_consume(self._on_response,
                                    no_ack=True,
                                    queue=self._callback_queue)

    def _on_response(self, ch, method, props, body):
        if self._correlation_id == props.correlation_id:
            self._response = body
            LOG.info('got response: %s' % body)
        else:
            LOG.debug('Ignoring message w/ wrong correlation id')

    def call(self, func, *args, **kwargs):
        # TODO: remote exception handling
        self._response = None
        body = json.dumps(
            {'func_name': func.func_name,
             'args': args,
             'kwargs': kwargs})
        self._correlation_id = str(uuid.uuid4())

        self._channel.basic_publish(exchange='',
                                    routing_key='mytwitter.amqp.queue',
                                    properties=pika.BasicProperties(
                                        reply_to=self._callback_queue,
                                        correlation_id=self._correlation_id),
                                    body=body)
        return self._get_result()

    def _get_result(self):
        try:
            while self._response is None:
                self._conn.process_data_events()
        except Exception:
            import pdb
            pdb.set_trace()
        return self._response
