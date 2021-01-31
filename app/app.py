from flask.app import *
from flask.templating import render_template
from pykafka.client import KafkaClient
from pykafka.exceptions import NoBrokersAvailableError
import flask
import time

app = Flask(__name__)


def get_kafka_client(hosts):
    return KafkaClient(hosts=hosts)


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
        cosumered_data = consumer.consume()
        if cosumered_data is not None:
            return jsonify(data=cosumered_data.value.decode("utf-8"))
        time.sleep(2)


@app.route('/', methods=['GET', 'POST'])
def conversation():
    if flask.request.method == 'GET':
        return render_template('main.html')
    elif flask.request.method == 'POST':
        return render_template('main.html')


@app.route('/firstUserSendData', methods=['POST', 'GET'])
def first_user_send_data():
    if flask.request.method == 'GET':
        return render_template('first_topic.html')
    elif flask.request.method == 'POST':
        data = request.form['textToSend']
        data_to_send_to_topic = ('{"sender": 1, "message": "%s"}' % data)
        conversation_producer.produce(data_to_send_to_topic.encode("utf-8"))
        sender_1_producer.produce(data_to_send_to_topic.encode("utf-8"))
        all_data.append(data_to_send_to_topic)
        return flask.Response(status=204)


@app.route('/secondUserSendData', methods=['POST', 'GET'])
def second_user_send_data():
    if flask.request.method == 'GET':
        return render_template('second_topic.html')
    elif flask.request.method == 'POST':
        data = request.form['textToSend']
        data_to_send_to_topic = ('{"sender": 2, "message": "%s"}' % data)
        conversation_producer.produce(data_to_send_to_topic.encode("utf-8"))
        sender_2_producer.produce(data_to_send_to_topic.encode("utf-8"))
        all_data.append(data_to_send_to_topic)
        return flask.Response(status=204)


@app.route('/getAllData', methods=['GET'])
def get_all_data():
    return {"data": all_data}


@app.route('/getTopicDataFromSender1', methods=['GET'])
def get_second_topic_data():
    return get_topic_data(sender_1_consumer)


@app.route('/getTopicDataFromSender2', methods=['GET'])
def get_first_topic_data():
    return get_topic_data(sender_2_consumer)


if __name__ == '__main__':

    kafka_client_address = os.getenv("KAFKA_ADVERTISED_HOST_NAME")
    kafka_port = os.getenv("KAFKA_PORT")
    client_address = kafka_client_address + ":" + kafka_port
    print("Conecting to kafka on: " + client_address)

    # This needs refactoring!
    waitingForKafka = True
    while waitingForKafka:
        try:
            client = get_kafka_client(client_address)
            break
        except NoBrokersAvailableError:
            print("Failed to connect to kafka")
    conversation_consumer = create_kafka_consumer(client, "conversation")
    conversation_producer = create_kafka_producer(client, "conversation")
    sender_1_consumer = create_kafka_consumer(client, "sender_1")
    sender_1_producer = create_kafka_producer(client, "sender_1")
    sender_2_consumer = create_kafka_consumer(client, "sender_2")
    sender_2_producer = create_kafka_producer(client, "sender_2")
    all_data = [msg.value.decode("utf-8") for msg in conversation_consumer]
    app.run(port=5000, debug=True, host='0.0.0.0')
