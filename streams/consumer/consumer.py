import os
import json
from kafka import KafkaConsumer

print("Consuming messages on " + os.environ['TOPIC'] + " from " + os.environ['BOOTSTRAP_SERVER'])

# This script receives messages from a Kafka topic


consumer = KafkaConsumer(
    os.environ['TOPIC'],
    auto_offset_reset="earliest",
    bootstrap_servers=os.environ['BOOTSTRAP_SERVER'],
    #client_id="py-demo-goup",
    group_id="py-demo-group",
    security_protocol="SSL",
    ssl_cafile=os.environ['PATH_TO_CERT']+"/ca.pem",
    ssl_certfile=os.environ['PATH_TO_CERT']+"/access.cert",
    ssl_keyfile=os.environ['PATH_TO_CERT']+"/access.key",
    value_deserializer=lambda m: int('0x' + m.hex().lstrip('0'), 0),
    key_deserializer=lambda k: k.decode('utf-8')
)

# Call poll twice. First call will just assign partitions for our
# consumer without actually returning anything

#for _ in range(2):
while True:
    raw_msgs = consumer.poll(timeout_ms=1000)
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            print("Received: {} {}".format(msg.key, msg.value))
    consumer.commit()

# Commit offsets so we won't get the same messages again

