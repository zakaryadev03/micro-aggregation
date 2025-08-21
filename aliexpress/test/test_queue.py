import pika
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

connection = pika.BlockingConnection(
    pika.URLParameters(os.getenv("RABBITMQ_URL"))
)
channel = connection.channel()


channel.queue_declare(queue="product_searches", durable=True)
channel.queue_declare(queue="price_updates", durable=True)


test_queries = [
    {"keyWord": "iphone"},
    {"keyWord": "laptop"}
]

for query in test_queries:
    channel.basic_publish(
        exchange="",
        routing_key="product_searches",
        body=json.dumps(query),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"➡️ Sent query: {query['keyWord']}")


print("\n⏳ Waiting for services (AliExpress & Amazon) to send results...")
time.sleep(5)  


print("\n📥 Sneak peek at 'price_updates':")
max_peek = 5
count = 0

for i in range(max_peek):
    method_frame, header_frame, body = channel.basic_get(queue="price_updates", auto_ack=False)
    if method_frame:
        count += 1
        try:
            message = json.loads(body.decode())
        except Exception:
            message = body.decode()
        print(f"Result {count}: {message}")
        # Put it back
        channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=True)
    else:
        break

if count == 0:
    print("No results found yet.")

connection.close()
print("\n done")
