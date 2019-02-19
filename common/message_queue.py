import pika
import logging
import time


class MessageQueue:
    EXCHANGE_NAME = "rra-direct"

    def __init__(self, queue_names = None, host="localhost", delay=5.0):
        self.delay = delay
        self.logger = logging.getLogger(self.__class__.__name__)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.queues = {}
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.EXCHANGE_NAME,
                                      exchange_type="direct")
        if queue_names is not None:
            for queue_name in queue_names:
                self.add_queue(queue_name)

    def send_message(self, message, routing_key):
        self.channel.basic_publish(exchange=self.EXCHANGE_NAME,
                                   routing_key=routing_key,
                                   body=message)
        self.logger.debug("Message : %s sent" % message)

    def receive_message(self, queue_name):
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)

        while method_frame is None or method_frame.NAME == 'Basic.GetEmpty':
            method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
            time.sleep(self.delay)

        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body

    def bind(self, queue_name, routing_key):
        if queue_name in self.queues.keys():
            self.channel.queue_bind(exchange=self.EXCHANGE_NAME,
                                    queue=queue_name,
                                    routing_key=routing_key)
        else:
            self.logger.error("Queue %s not found" % queue_name)

    def add_queue(self, queue_name):
        if queue_name not in self.queues.keys():
            self.queues[queue_name] = self.channel.queue_declare(queue=queue_name)
        else:
            self.logger.error("Queue %s already exists" % queue_name)

