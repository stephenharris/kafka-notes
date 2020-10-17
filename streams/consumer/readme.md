docker build -t consumer .

docker run --env-file .env \
-v /home/stephen/Documents/Development/kafka/streams/store:/etc/cert \
consumer