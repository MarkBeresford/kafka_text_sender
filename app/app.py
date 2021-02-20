from flask.templating import render_template
import flask
from kafka_topic_util import *

app = Flask(__name__)

kafka_client = connect_to_kafka_client()

all_conversation_data = []

conversation_consumer = create_kafka_consumer(kafka_client, "conversation")
sender_1_consumer = create_kafka_consumer(kafka_client, "sender_1")
sender_2_consumer = create_kafka_consumer(kafka_client, "sender_2")

conversation_producer = create_kafka_producer(kafka_client, "conversation")
sender_1_producer = create_kafka_producer(kafka_client, "sender_1")
sender_2_producer = create_kafka_producer(kafka_client, "sender_2")


@app.route('/', methods=['GET', 'POST'])
def conversation():
    if flask.request.method == 'GET':
        return render_template('main.html')
    elif flask.request.method == 'POST':
        return render_template('main.html')


@app.route('/UserSendData/<user>', methods=['POST', 'GET'])
def second_user_send_data(user):
    if flask.request.method == 'GET':
        if user == '1':
            print("first_topic")
            return render_template('first_topic.html')
        else:
            print("second_topic")
            return render_template('second_topic.html')
    elif flask.request.method == 'POST':
        data = request.form['textToSend']
        data_to_send_to_topic = ('{"sender": %s, "message": "%s"}' % (user, data))
        if user == '1':
            sender_1_producer.produce(data_to_send_to_topic.encode("utf-8"))
        else:
            sender_2_producer.produce(data_to_send_to_topic.encode("utf-8"))

        conversation_producer.produce(data_to_send_to_topic.encode("utf-8"))
        all_conversation_data.append(data_to_send_to_topic)
        return flask.Response(status=204)


@app.route('/getTopicData/<user>', methods=['GET'])
def get_second_topic_data(user):
    if user == '1':
        return get_topic_data(sender_1_consumer)
    else:
        return get_topic_data(sender_2_consumer)


@app.route('/getAllData', methods=['GET'])
def get_all_data():
    all_data = [msg.value.decode("utf-8") for msg in conversation_consumer]
    all_conversation_data.append(all_data)
    return {"data": all_conversation_data}


@app.route('/recreateAllTopics', methods=['GET'])
def recreate_all_topics():
    all_conversation_data.clear()
    print(all_conversation_data)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
