import pika
import json

class UserEventProducer:
    def __init__(self, queue_name="user_registered"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name)

    def publish_event(self, event):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(event)
        )
        print(f"[x] Published event to {self.queue_name}: {event}")

    def close(self):
        self.connection.close()