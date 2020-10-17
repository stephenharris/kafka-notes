# Consumer Groups

Consumers are single threaded, and so represent a bottleneck.

Consumer Groups allow you to scale out consumers, but in a way that they work together. 

A consumer group consists of independent consumers assigned to the same group (`group.id`). The task of processing records from a topic is then shared evenly across the consumers.

 - parallelism increases throughput (we can increase number of records that can be processed per second)
 - introduces reudnancy of consumers (e.g. if one consumer goes down, record processing doesn't stop)
 - improved performance (can process backlog of records more quickly)



## Group co-ordinator

A broker is elected to be group co-ordinator.
Montiors group membership, and assign individual paritions to a consumer in the group.
The group cordinator uses the 'heartbeat' of the individual consumers (send every `heartbeat.interval.ms` ms) to determine which consumers are alive and can participate in the group. If a consumer fails to send a heartbeat within `session.timeout.ms` the co-ordinator will assign the consumer's parition(s) to others in the group.

Adding/removing consumers/paritions will also trigger a rebalance by the co-ordinator.
It will try to achieve 1:1 consumer-to-parition ratio, but if paritions < consumers, some consumers will be left idle.




