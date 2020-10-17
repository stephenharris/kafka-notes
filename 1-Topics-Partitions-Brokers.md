## Topics

Topics are essentially a named feed or category of messages
Logical entity
Consumes consume from a topic

Each topic has its own log

Topics can spean across multiple brokers. Producers simply publish to a topic - they don't care which broker(s?) handle it. Likewise consumers just consume a topic, they don't care about which broker(s) have handled the message.

When a producer 'publishes' a message, it has appended to a time-ordered, immutable sequence of messages/events.


## Message

A message has a

 - timestamp (assigned by the broker)
 - Referencable identifier
 - The message payload (binary)


## Consumers

Consumers maintain their own 'offset' - this acts as a indicator of the last read message position. In fact its the referencable identifier of the message.

When a consumer connects to the broker, they provide their offset to indicate where they want to recieve messages from. This allows kafka to support 'slow consumers' as events are retained (as per message retention policy) for a certain period of time. Within that time frame, consumers can consume messages at their own rate. Default is 7 days, and defined on a per-topic message.


# Transaction or Commit Logs

- Commit log is the 'source of truth'
- new events are appended, and the log is immutable
- can replay events from a point in time


*Apache Kafka is publish-subscribe messaging rethought as a distributed commit log*


## Parition

Each topic has one or more paritions
A parition must be wholly contained within a broker (but might be duplicated across multiple brokers)

Partioning allows you to essentially split your topic across different broker nodes, and thus scale horizontally.

Brokers are selected, and each partition is assigned to a broker (possibly replicated?). Each partition maintains its own independent commit log. (commit log replicated too?)

When publishing a producer needs to know at least one broker in the cluster (or does it have to be one with at least one parition??). Each broker knows who is the loader for the parition the message should be written to and communicates that back to the producer so that they can send messages to the appropriate brokers.

Consumers integrate the zookeeper to find out which brokers own which paritions, and queries those brokers for the latest events (since offset). However, as messages are spread across multiple partitions, its possible that the consuemr will recieve them out-of-order, and the client needs to handle that (question: do consumer libraries handle that, or does that need to be handled at application layer?)

Trade-offs:

 - Paritions allow you to scale horizontally
 - more paritions, the greater the zookeper overhead
 - if you have > 1 paritions you loose global ordering (needs to be handled by the consumer)
 - the more paritions the longer the leader fail-over time


How is fault tolerance handled. E.g.

 - Broker failure
 - Broker unreachable
 - Broker disk failure

Zookeeper monitors brokers, and if one goes down, it finds another to replace it. This allows kafka to continue, but without replication that broker's parition data will be lost. Replication (see replication factor) means that other brokers should have a copy of the data and it can be recovered.

The replication factor means that messages are replicated across multiple brokers. 2/3 is recommended. With RF of N you can survive N-1 broker failures. When this is set, the leader of the parition is responsible for finding brokers to duplicate the parition to, and establish a qurom. The number of in-sync replicas is referred to as the ISR number

