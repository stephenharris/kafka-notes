# Kafka Rollouts Demo

Demonstrating using Argo rollouts with kafka.


```
 -----------------                                                  -----                                                      ----------
| Initial producer | ---produces---> (rollout-test) ---consumes--> | App |  ---produces---> (rollout-test-out) ---consumes--> | Consumer |
 -----------------                                                  -----                                                      ----------
```

- `rollout-test` and `rollout-test-out` will have two paritions
- There will be two instances of App (the only differnece being a `VERSION` environment variable)
- An argo rollout will gradually replace each pod, pausing to perform metric analysis
- Initial producer / consumer are simple docker containers that are run locally
- It's expected there is a running clsuter - see [streams/readme.md](../streams/readme.md)


## Build & Publish

```
docker build -t stephenharris13/kafka-rollout-app app
# docker push stephenharris13/kafka-rollout-app
docker build -t kafka-rollout-consumer consumer
docker build -t kafka-rollout-producer producer
```

## Credentials

You will need your consumer's access key and certificate  (`access.key`, `access.cert`), as well as the broker certificate  (`ca.pem`). These shold be stored in a folder referenced below (in this example it is assmed it's in `../streams/store`).



## Running in a cluster

```
# Connect to cluster
aws eks --region eu-west-1 update-kubeconfig --name <<luster name>>

# Create kafka secrets
kubectl create secret generic kafka-secrets \
--from-file=ca.pem=../streams/store/ca.pem \
--from-file=access.cert=../streams/store/access.cert \
--from-file=access.key=../streams/store/access.key 

# Set-up argo rollouts
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://raw.githubusercontent.com/argoproj/argo-rollouts/stable/manifests/install.yaml

# Create rollout 
kubectl apply -f kafka-rollout.app.yaml

# Create prometheus
kubectl create configmap prometheus --from-file prometheus-config/prometheus.yml
kubectl apply -f prometheus.yaml
```

Kick-off the consumer & producer

```
docker run --env-file consumer/.env \
-v $PWD/../streams/store:/etc/cert \
kafka-rollout-consumer

docker run --env-file producer/.env \
-v $PWD/../streams/store:/etc/cert \
kafka-rollout-producer
```

To view the metrics:

```
kubectl port-forward svc/prometheus 9090
# Go to localhost:9090
# Run query sum by (version) (rate(processed_messages_total[1m]))
```

Change the `VERSION` environment variable and deploy:

```
kubectl apply -f kafka-rollout.app.yaml

# Watch the rollout
kubectl argo rollouts get rollout kafka-rollout-app  --watch

# Promote when ready
kubectl argo rollouts promote kafka-rollout-app
```
