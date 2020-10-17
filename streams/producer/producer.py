import os
from kafka import KafkaProducer
from time import sleep

print("Sending messages to " + os.environ['TOPIC'] + " on " + os.environ['BOOTSTRAP_SERVER'])

producer = KafkaProducer(
    bootstrap_servers=os.environ['BOOTSTRAP_SERVER'],
    security_protocol="SSL",
    ssl_cafile=os.environ['PATH_TO_CERT']+"/ca.pem",
    ssl_certfile=os.environ['PATH_TO_CERT']+"/access.cert",
    ssl_keyfile=os.environ['PATH_TO_CERT']+"/access.key",
)

iterations = int(os.getenv('ITERATIONS', '1'))

if iterations > 0 and iterations < 20000:
    for i in range(1, iterations + 1):
        message = "msg {}".format(i)
        print("Sending: {}".format(message))
        producer.send(os.environ['TOPIC'], message.encode("utf-8"))
        sleep(0.05)

# Force sending of all messages
producer.flush()
