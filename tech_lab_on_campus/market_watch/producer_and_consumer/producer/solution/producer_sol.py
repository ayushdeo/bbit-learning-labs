import os
import pika
from producer_interface import mqProducerInterface


class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        self.m_routing_key = routing_key
        self.m_exchange_name = exchange_name
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        connection_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.m_connection = pika.BlockingConnection(connection_params)
        self.m_channel = self.m_connection.channel()
        self.m_channel.exchange_declare(exchange=self.m_exchange_name)
    def publishOrder(self, message: str) -> None:
        self.m_channel.basic_publish(
            exchange=self.m_exchange_name,
            routing_key=self.m_routing_key,
            body=message.encode("utf-8")
        )
        self.m_channel.close()
        self.m_connection.close()