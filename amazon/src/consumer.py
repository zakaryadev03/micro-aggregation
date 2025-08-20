# consumer.py
from __future__ import annotations
import os
import json
import logging
import sys
from dotenv import load_dotenv
import pika

from amazon import AmazonAPI

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")


def main():
    params = pika.URLParameters(RABBITMQ_URL)
    try:
        conn = pika.BlockingConnection(params)
    except Exception as exc:
        logger.exception("Failed to connect to RabbitMQ: %s", exc)
        sys.exit(1)

    channel = conn.channel()

    # durable queues
    channel.queue_declare(queue="product_searches", durable=True)
    channel.queue_declare(queue="price_updates", durable=True)

    api = AmazonAPI()

    logger.info("Amazon service waiting for product_searches…")

    def callback(ch, method, properties, body):
        try:
            payload = json.loads(body.decode())
            keyWord = payload.get("keyWord")
            logger.info("→ [Amazon] Searching for: %s", keyWord)

            results = api.search_products(keyWord)
            if results and len(results):
                msg = json.dumps({"source": "Amazon", "data": results})
                # persistent delivery_mode=2
                ch.basic_publish(
                    exchange="",
                    routing_key="price_updates",
                    body=msg,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
                logger.info("✓ [Amazon] Sent %d items to price_updates", len(results))
            else:
                logger.warning("⚠️ [Amazon] No results or API error")
        except Exception:
            logger.exception("Error processing message")
        finally:
            # acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)  # fair dispatch
    channel.basic_consume(queue="product_searches", on_message_callback=callback, auto_ack=False)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Interrupted by user, shutting down...")
    finally:
        if not conn.is_closed:
            conn.close()


if __name__ == "__main__":
    main()
