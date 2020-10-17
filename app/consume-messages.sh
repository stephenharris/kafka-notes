#!/usr/bin/bash
# consumes messages

docker run --tty \
           --network app_default \
           confluentinc/cp-kafkacat \
           kafkacat -b app_kafka_1:9092 -C -K: \
                    -f '\nKey (%K bytes): %k\t\nValue (%S bytes): %s\n\Partition: %p\tOffset: %o\n--\n' \
                    -t UploadFile \
                    -o 1
