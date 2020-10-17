
## Getting set up


     docker-compose -f app/docker-composer.yml up


Then in a new window

    # list topics
    docker exec -it app_kafka_1 /opt/kafka/bin/kafka-topics.sh --zookeeper app_zookeeper_1:2181 --list
    # GetEmailContent
    # GetFile
    # TrackUpload
    # UploadFile
    # __consumer_offsets


Describe the `__consumer_offsets`

    docker exec -it app_kafka_1 /opt/kafka/bin/kafka-topics.sh --zookeeper app_zookeeper_1:2181 --describe --topic __consumer_offsets


To run a consumer:

     ./app/consumer-messages.sh


To publish some messages

     ./app/publish-message.sh