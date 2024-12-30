import pika
import json

class PaymentEventConsumer:
    def __init__(self, queue_name="payment_processed"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name)

    def start_consuming(self, callback):
        def on_message(ch, method, properties, body):
            event = json.loads(body)
            callback(event)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=on_message, auto_ack=True)
        print(f"[*] Waiting for events on {self.queue_name}")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()