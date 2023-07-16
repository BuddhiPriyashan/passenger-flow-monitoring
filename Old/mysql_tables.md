mysql> show tables;
+-----------------------------------+
| Tables_in_passenger_flow_counts   |
+-----------------------------------+
| passenger_count                   |
| passenger_count_epochtime         |
| passenger_count_epochtime_grafana |
+-----------------------------------+

mysql> select * from passenger_count;
+------------+------------+-------+
| operator   | vehicle_id | count |
+------------+------------+-------+
| Operator-1 | AB123      |  8023 |
| Operator-2 | CD394      |     0 |
| Operator-3 | PR980      |     0 |
+------------+------------+-------+

mysql> select * from passenger_count_epochtime;
+------------+------------+-------+------------+
| operator   | vehicle_id | count | epoch_time |
+------------+------------+-------+------------+
| ASTRA GmbH | 111222333  |   769 | 1689429238 |
+------------+------------+-------+------------+

mysql> select * from passenger_count_epochtime_grafana;
+------------+------------+-------+------------+
| operator   | vehicle_id | count | epoch_time |
+------------+------------+-------+------------+
| ASTRA GmbH | 111222333  |   148 | 1689255688 |
| ASTRA GmbH | 111222333  |   149 | 1689255688 |
| ASTRA GmbH | 111222333  |   150 | 1689255692 | <- counter reset
| ASTRA GmbH | 111222333  |     1 | 1689261064 |
| ASTRA GmbH | 111222333  |     2 | 1689261065 |
| ASTRA GmbH | 111222333  |    30 | 1689261093 |
| ASTRA GmbH | 111222333  |    31 | 1689261093 |
| ASTRA GmbH | 111222333  |    32 | 1689261094 | <-counter reset
| ASTRA GmbH | 111222333  |     1 | 1689353157 |
| ASTRA GmbH | 111222333  |     2 | 1689353157 |
| ASTRA GmbH | 111222333  |     9 | 1689353162 |
| ASTRA GmbH | 111222333  |    10 | 1689353162 |
| ASTRA GmbH | 111222333  |    11 | 1689353163 |
| ASTRA GmbH | 111222333  |     1 | 1689364739 |
| ASTRA GmbH | 111222333  |     2 | 1689364739 |
| ASTRA GmbH | 111222333  |    29 | 1689366054 |
| ASTRA GmbH | 111222333  |    30 | 1689371527 |
| ASTRA GmbH | 111222333  |    27 | 1689429238 |
| ASTRA GmbH | 111222333  |    28 | 1689429238 |
+------------+------------+-------+------------+