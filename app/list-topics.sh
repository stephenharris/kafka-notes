#!/usr/bin/bash
# lists all topics 
docker run --tty \
           --network app_default \
           confluentinc/cp-kafkacat \
           kafkacat -b app_kafka_1:9092 \
                    -L
