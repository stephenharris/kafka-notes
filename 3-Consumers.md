# Consumers

Consumers also get a list of broker servers.
A consumer can subscribe to one or more topics. (You can even subscribe using regular expressions!) - "subscribe"
By default the consumer will poll all partitions for each topic
You can also subscribe to specific topic partition - "assign"


## Poll loop

When consumer subscribe/assign is called the SubscrptiontState is initialised (includes offsets?)
When poll is invoked, the consumer calls one of the brokers to get the cluster metadata (paritions, partiton owners)
Consumer then sends 'heartbeats'. This lets the cluster know which consumers are connected. It also keeps cluster information held in the consumer up to date.
Consumers continously poll the brokers for new records.


Note: the poll process is **single threaded**. There is only one poll loop (and one thread) per consumer.


## Offset

Each consumer will have an offset for each partition it is subscribed to.

**last committed offset** - last record that consumer has confirmed its processed

As the consumer reads recommends it will record its **current position** until it reaches the **log-end offset**. There is potentially a gap which forms between the last committed offset and the current position - which represented un-committed offsets.

By default Kafka will auto-commit records every 5 seconds - even if your application code has actually processed the record.

     enable.auto.commit = true # (default)
     auto.commit.interval.ms = 5000 # (default)
     auto.offset.reset = "latest" # (default) start from earliest commited offset

Increasing the interval might be commits lag behind actually processed records, while the reverse is strue if its decreased. A failure might see records seen twice or records missed.

To switch to 'manual' mode

     enable.auto.commit = false

This gives you full control of when a record is committed using

    commitSync
    commitAsync

The `commitSync` method is used for when you want to make sure that you do not continue to process new records until you have confirmed that the records you have processed have been committed. It is recommend you do this in at the end of a for loop, not within - which would just add extra latency and might not buy you much.
As the name suggests, the call is syncronous and will block the thread until it recieves a respons from the cluster. `commitSync` will automatically retry failed commits. This trades consistency for throughput.

The `commitAsync` is non-blocking. You may not know when a commit is successful, for this reason it doesn't automatically retry, but you can manually retry in a callback which is called when that response is recieved. This approach improves throughput at the expense of consistency - you may continue to process records before confirming that the previous record has been commmited.

Using the commit API you can:

 - control consistency ("when it is done")
 - atomicity (treating record fetching and process as a single atomic operation). Achieve "exactly once".

The offset is stored in a topic `__consumer_offsets`



## Consumer configuration

 **fetch.min.bytes** - Minimum number of bytes that must be returned in the poll. This effectively ensures you have a certain amount of records to process before processing them. This is analgous to the batch size on the producer side
 **max.fetch.wait.ms** - maximum time to wait for sufficient data to be available as per fetch.min.bytes until records are fetched anyway (analgous to linger.ms in producer)
 **max.parition.fetch.bytes** - maximum number of bytes returned (per cycle, per parition) - helps ensure that you are not consuming more data than you can safely process in each poll cycle.
 **max.poll.records** - maximum number of records that are returned per poll cycle


