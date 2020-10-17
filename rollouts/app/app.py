import os
import json
from kafka import KafkaProducer, KafkaConsumer
import prometheus_client as prom
from threading import Thread
from flask import Flask
from flask_prometheus import monitor

print("Consuming messages on " + os.environ['CONSUME_TOPIC'] + " and write to " + os.environ['PRODUCE_TOPIC'])
print("Running on kafka cluster " + os.environ['BOOTSTRAP_SERVER'])

counter = prom.Counter('processed_messages', 'This is my counter', ['version'])

app = Flask("pyProm")
 
consumer = KafkaConsumer(
    os.environ['CONSUME_TOPIC'],
    auto_offset_reset="earliest",
    bootstrap_servers=os.environ['BOOTSTRAP_SERVER'],
    group_id="rollouts-demo-group",
    security_protocol="SSL",
    ssl_cafile=os.environ['PATH_TO_CERT']+"/ca.pem",
    ssl_certfile=os.environ['PATH_TO_CERT']+"/access.cert",
    ssl_keyfile=os.environ['PATH_TO_CERT']+"/access.key",
    value_deserializer=lambda m: m.decode('utf-8'),
)

producer = KafkaProducer(
    bootstrap_servers=os.environ['BOOTSTRAP_SERVER'],
    security_protocol="SSL",
    ssl_cafile=os.environ['PATH_TO_CERT']+"/ca.pem",
    ssl_certfile=os.environ['PATH_TO_CERT']+"/access.cert",
    ssl_keyfile=os.environ['PATH_TO_CERT']+"/access.key",
)

def thr():
    while True:
        raw_msgs = consumer.poll(timeout_ms=1000)
        for tp, msgs in raw_msgs.items():
            for msg in msgs:
                print("Received: {}".format(msg.value))
                message = "processed {} in version {}".format(msg.value, os.environ['VERSION'])
                print("Sending: {} to {}".format(message, os.environ['PRODUCE_TOPIC']))
                producer.send(os.environ['PRODUCE_TOPIC'], message.encode("utf-8"))
                producer.flush()
                # Report to prometheus
                counter.labels(version=os.environ['VERSION']).inc(1)
        consumer.commit()

Thread(target=thr).start()
monitor(app, port=8080)
