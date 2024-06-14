import time
import numpy as np
import json
import pika
import uuid
from camera import Camera


class Client:
    def __init__(self, hostname='localhost', queuename='rpc_queue'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        self.response = None
        self.corr_id = None
        self.queuename = queuename

    def on_response(self, channel, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def serialize(self, json_data):
        return json.dumps(json_data)
    
    def deserialize(self, serialized_json_body):
        deserialized_data = json.loads(serialized_json_body)
        return deserialized_data

    def predict(self, np_data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key=self.queuename, properties=pika.BasicProperties(
            reply_to=self.callback_queue, correlation_id=self.corr_id,),
            body=self.serialize({
                'array': np_data.tolist(),
                'message': 'classification'
            })
        )
        self.connection.process_data_events(time_limit=None)
        return self.deserialize(self.response)


if __name__ == '__main__':
    client = Client()
    camera_simulator = Camera(data_path="../../training/data/data_6_fps", frame_size=128, load_dump=True)

    while True:
        # clip = camera_simulator.get_clip()
        clip = camera_simulator.get_clip_real_cam()
        t0 = time.time()
        predict = client.predict(clip)
        t1 = time.time()
        print(predict)
        print(t1 - t0, "sec")
        time.sleep(5) # sec