import os
import json
from kafka import KafkaConsumer

print("Consuming messages on " + os.environ['TOPIC'] + " from " + os.environ['BOOTSTRAP_SERVER'])

consumer = KafkaConsumer(
    os.environ['TOPIC'],
    auto_offset_reset="earliest",
    bootstrap_servers=os.environ['BOOTSTRAP_SERVER'],
    group_id="py-test-consumer",
    security_protocol="SSL",
    ssl_cafile=os.environ['PATH_TO_CERT']+"/ca.pem",
    ssl_certfile=os.environ['PATH_TO_CERT']+"/access.cert",
    ssl_keyfile=os.environ['PATH_TO_CERT']+"/access.key",
    value_deserializer=lambda m: m.decode('utf-8'),
)

while True:
    raw_msgs = consumer.poll(timeout_ms=1000)
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            print("Received: {}".format(msg.value))
    consumer.commit()