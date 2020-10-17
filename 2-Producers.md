# Producers

- Producers are given a set of brokers
- Producer will find first available to connect to, it will then use that broker to discover cluster membership & partition leaders
- We provide multiple brokers in case the first is not available

Producers sends 'ProducerRecords'. A ProducerRecords consists of:

 - topic: the topic to which the record will be sen
 - value: the user-defined payload (type sensitive).*
 - partion: specific parition within the topic to send the record to
 - timestamp: unix timestamp applied to the record (long type, adds 8 bytes to record!). Default is created time**. 
 - key: can be used to contain additional information; if present determines the parition 

*Kafka producers can only send ProducerRecords that match the key and value serializers types it is configured with.

** You can confgure the broker to use LogAppendTime and it will use the time its committed to the log - ignoring the producer set time.



When sending a record:
 
1. Producer uses an available broker to discover cluster membership & parition ownership
2. Passes method through the serializer
3. Producer determines what parition to send the record to
    - If 'partition' is set and valid use that (exceptions if not)
    - If it has a 'key' uses mod-hash strategy (unless some custom paritioning logic is provided by Producer_Class_Config)
    - Otherwise uses round-robin


Messages are buffered to improve effeciency. Each topic-partition pair has their own batch. Records are added to the batch and are sent when
 - total buffer size reaches per-buffer batch.size limit, OR
 - timelimit is reached (linger.ms)

Each batch has a limit on the total memory of records it can hold (batch.size - max amount of bytes that can be buffered). There is also a global limit (buffer.memory) across all batches. If this global limit is reached, the producer will be blocked from sending for `max.block.ms` milliseconds.

When batches are sent, the broker will respond with RecordMetadata.


Delivery guarantees

 - Producer can sepcify "acks" (level of broker acknowledgement:
   - 0: fire & forget, no acknowledgement
   - 1: leader acknowledged
   - 2: replication quorum acknowledged (all replicas confirm). Highlest level of assururence, but takes longer

If a broker resopnds with an error you can configure how the producer resonds:

  - retries - number of times it retries to send records
  - retry.backoff.ms - wait period in ms between retries


Ordering guranteeies

 - message orders is only preserved within a parition
 - retries might cause message to go out-of-sync. You can set max.in.flight.request.per.connection to 1 which avoids this problem by allowing a producer to send only one request a time. But these greatly throttles throughput.


