# Architecture

 - Publish/subscribe messaging system
 - publisher ("producers") sends message to a particular location - a topic
 - subscribers ("consumers") will listen for these messages and consumer them
 - brokers manages the topics
 - Brokers can be scaled horizontally, and form a cluster. A kafka cluster is a grouping of kafka brokers - which might or might not be on the same machine.



## Distributed systems

 - collection of resourceses that are instructed to achieve a specific goal
 - consist of multiple nodes
 - nodes require co-ordinate to ensure consistency and progress towards common goal
 - each node commmunciates with each other
 
A controller is a node like any other, but is selected to maintain
 - list of work items
 - status of workers nodes
 - list of nodes

Controller monitors
 - which nodes are available and healthy
 - take account of redunancy policies (replication factor)


Replication factor

 - To ensure work is not lost we can specify a replication factor (e.g. 3)
 - Controller will select a "leader" node who will take ownship of the message/item
 - leader will recruit other worker nodes to take part in replication - they form a quoram
 

In kafka "work item" is recieving messages, categorising them and persisting them for future retrieval


## Apache zookeeper

Centralised service for maintaing metadata about a cluster of nodes:
 - health status
 - group membership
 - configuration information

The zookeper is itself a distributed system called an 'ensembled'





