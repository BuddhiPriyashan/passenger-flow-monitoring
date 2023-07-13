#start counter 
bdy@uburasp1:~/push_to_mysql$ sudo python3 edge-to-mysql.py

#start webapp
bdy@uburasp2:~/query_mysql$ sudo python3 webapp.py

#verify with MySQL db if results are correct
bdy@uburasp2:~$ mysql -u webappusr -h 192.168.1.129 -p
mysql> USE passenger_flow_counts
mysql> SELECT * from passenger_count;

#open page in browser
http://192.168.1.129:5000/

#Build the Docker container form the Docker file
bdy@uburasp2:~/query_mysql$ sudo docker build -t iot/webapp:1.5 .

#Run the docker container
sudo docker run -p 5000:5000 iot/webapp:1.5

INSERT INTO passenger_count_epochtime ( operator, vehicle_id, count, epoch_time) VALUES ( 'Operator-1', '111222333', '0', '1689192443' );
UPDATE passenger_count_epochtime SET operator = 'ASTRA GmbH' WHERE operator = 'Operator-1';


#A Grafana Query
SELECT count AS value, epoch_time AS time FROM passenger_flow_counts.passenger_count_epochtime WHERE operator='ASTRA GmbH';