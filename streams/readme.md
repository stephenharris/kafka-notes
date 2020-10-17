# Streaming application with Aiven

## Keystore & Truststore
To authenticate with the Aiven broker the client needs to use a certificate `access.cert` and to encrypt trafic needs the corresponding private key `access.key`. These can be downloaded from Aiven dashboard. For Java based applications they need to be loaded into a key store:

    openssl pkcs12 -export -inkey access.key -in access.cert -out client.keystore.p12 -name service_key
    # To retrieve the private key & cert from the key store
    # openssl pkcs12 -info -in client.keystore.p12 -nodes > out.txt

Next to authenticate and decrypt responses we need the broker's certificate (which also can be downloaded from Aiven dashboard). This certificate needs to be loaded into a truststore:

    keytool -import -file ca.cert -alias CA -keystore client.truststore.jks
    # To retrieve the certificate from the trustore
    # keytool -export -file ca.cert -alias CA -keystore client.truststore.jks

Both the keystore and truststore are password protected.

Update `kafka.config` with the appropriate values. The keys, certificates and stores should be put in `streams/store`.

## Create topics

Create `test` and `test-output`

## Producer/Consumer test (optional)

TODO download instructions

Run the producer
```
./bin/kafka-console-producer.sh --bootstrap-server kafka-3ca2c5e3-stephenh1988-adba.aivencloud.com:11435 \
    --producer.config /home/stephen/Documents/Development/kafka/streams/kafka.config \
    --topic test
```

Run the consumer
```
bin/kafka-console-consumer.sh --bootstrap-server kafka-3ca2c5e3-stephenh1988-adba.aivencloud.com:11435 \
    --consumer.config /home/stephen/Documents/Development/kafka/streams/kafka.config \
    --topic test-output \
    --from-beginning \
    --formatter kafka.tools.DefaultMessageFormatter \
    --property print.key=true \
    --property print.value=true \
    --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer \
    --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer
```

## Cluster


```
AWS_PROFILE=sparktest terraform init terraform/
AWS_PROFILE=sparktest terraform apply --var-file=terraform/test.tfvars terraform/
```

```
AWS_PROFILE=sparktest aws eks --region eu-west-1 update-kubeconfig --name kstream-wordcount
```

Create secret for key and trust store:

```
kubectl create secret generic storepwd --from-literal=truststore=secret --from-literal=keystore=secret

kubectl create secret generic store --from-file=client.keystore.p12=store/client.keystore.p12 --from-file=client.truststore.jks=store/client.truststore.jks
```

Create the wordcount pods

```
kubectl apply -f kstreams-wordcount.statefulset.yaml
```

### Consuming topics

```
docker build -t consumer consumer

docker run --env-file consumer/.env \
-v /home/stephen/Documents/Development/kafka/streams/store:/etc/cert \
consumer
```

### Producing topics

```
docker build -t producer producer

docker run --env-file producer/.env \
-v /home/stephen/Documents/Development/kafka/streams/store:/etc/cert \
producer
```
