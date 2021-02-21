from flask.app import *
import time
from pykafka.client import KafkaClient
from pykafka.exceptions import NoBrokersAvailableError


def create_kafka_consumer(client, topic_name):
    topic = client.topics[topic_name]
    consumer = topic.get_simple_consumer(consumer_timeout_ms=5000)
    return consumer


def create_kafka_producer(client, topic_name):
    topic = client.topics[topic_name]
    producer = topic.get_producer()
    return producer


def get_topic_data(consumer):
    while True:
        consumed_data = consumer.consume()
        if consumed_data is not None:
            return jsonify(data=consumed_data.value.decode("utf-8"))


def consume_all_data_on_conversation_history(conversation_consumer):
    all_data = [msg.value.decode("utf-8") for msg in conversation_consumer]
    all_conversation_data = all_data
    return {"data": all_conversation_data}



def connect_to_kafka_client():
    kafka_client_address = os.getenv("KAFKA_ADVERTISED_HOST_NAME")
    kafka_port = os.getenv("KAFKA_PORT")
    client_address = kafka_client_address + ":" + kafka_port
    while True:
        time.sleep(5)
        try:
            client = KafkaClient(hosts=client_address)
            print("Connected to Kafka!")
            return client
        except NoBrokersAvailableError:
            print("Failed to connect to kafka")
