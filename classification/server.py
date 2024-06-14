import pika
from classification import predict
from api_helpers import *
import numpy as np
import json
import pickle


def read_label_encoder():
    with open("../shared/label_encoder.picle", "rb") as file:
        loaded_data = pickle.load(file)
    return loaded_data

class ClassificationServer:
    def __init__(self, hostname='localhost', queue='rpc_queue'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.queue = queue
        self.label_encoder = read_label_encoder()
        self.class_count = 10
        self.labels = self.label_encoder.inverse_transform([i for i in range(self.class_count)])
        self.API = API()
        self.API.login()

    def predict(self, np_data):
        return predict(np_data)

    def deserialize(self, serialized_json_body):
        deserialized_data = json.loads(serialized_json_body)
        return deserialized_data

    def serialize(self, json_data):
        return json.dumps(json_data)

    def decode_predict(self, predict):
        decoded_predict = {}
        for i in range(self.class_count):
            decoded_predict[self.labels[i]] = predict.tolist()[0][i]
        return decoded_predict

    def make_gif(self, frames):
        frames = frames[0]
        gif_buffer = io.BytesIO()
        imageio.mimsave(gif_buffer, frames, format='GIF', fps=6)
        gif_buffer.seek(0)
        return base64.b64encode(gif_buffer.read()).decode('utf-8')

    def on_message(self, channel, method, props, body):
        try:
            json_data = self.deserialize(body)
            predict = self.predict(np.array([json_data['array']]))
            predict = self.decode_predict(predict)
            channel.basic_publish(exchange='', routing_key=props.reply_to,
                                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                                body=self.serialize(predict))
            channel.basic_ack(delivery_tag=method.delivery_tag)
            predict["type"] = max(predict, key=predict.get)
            fragment_id = self.API.save_fragment(np.array([json_data['array']]))
            self.API.save_log(predict, fragment_id)
        except Exception as e:
            print(e)

    def run_server(self):
        print('starting...')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_message)
        self.channel.start_consuming()

    def stop_server(self):
        if self.connection:
            self.connection.close()

if __name__ == '__main__':
    classification_server = ClassificationServer()
    classification_server.run_server()
