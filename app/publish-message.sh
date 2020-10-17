#!/usr/bin/bash
# publish messages

docker run --interactive \
           --network app_default \
           confluentinc/cp-kafkacat \
            kafkacat -b app_kafka_1:9092 \
                    -t UploadFile \
                    -K: \
                    -P <<EOF
1:FOO
2:BAR
EOF
