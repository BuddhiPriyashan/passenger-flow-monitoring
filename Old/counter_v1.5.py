###################################################################################################
##  Raspberry Pi Passenger Counter 
##
## 'passenger_count_epochtime_grafana' table from 'passenger_flow_counts' MySQL database
##         mysql> select * from passenger_count_epochtime_grafana where epoch_time > 1689454492;
##         +------------+------------+-------+------------+
##         | operator   | vehicle_id | count | epoch_time |
##         +------------+------------+-------+------------+
##         | ASTRA GmbH | 111222333  |   940 | 1689454493 |
##         | ASTRA GmbH | 111222333  |   941 | 1689454493 |
##         | ASTRA GmbH | 111222333  |   942 | 1689455412 |
##         | ASTRA GmbH | 111222333  |   943 | 1689455412 |
##         | ASTRA GmbH | 111222333  |   944 | 1689455414 |
##         | ASTRA GmbH | 111222333  |   945 | 1689455417 |
##         +------------+------------+-------+------------+
##         
##         
## 'passenger_count_epochtime' table from 'passenger_flow_counts' MySQL database
##         mysql> select * from passenger_count_epochtime;
##         +------------+------------+-------+------------+
##         | operator   | vehicle_id | count | epoch_time |
##         +------------+------------+-------+------------+
##         | ASTRA GmbH | 111222333  |   945 | 1689455417 |
##         +------------+------------+-------+------------+
##         
###################################################################################################

import mysql.connector 
import RPi.GPIO as GPIO
import time

sensor_pin = 2
counter = 0
operator_name = 'ASTRA GmbH'
vehicle_num = 111222333

db_config = {
    'host' : '192.168.1.129',
    'user' : 'piusr',
    'password' : 'piusr',
    'database' : 'passenger_flow_counts'
}

# Function to UPDATE the counter value of the 'passenger_count_epochtime' table
def update_counter(count):
    connection = mysql.connector.connect(**db_config)
    mycursor = connection.cursor()
    update_counter_query = 'UPDATE passenger_count_epochtime SET count = count + 1, epoch_time = %s WHERE operator = %s AND vehicle_id = %s'
    eptime = int(time.time())
    mycursor.execute(update_counter_query, (eptime,operator_name,vehicle_num))
    connection.commit()
    mycursor.close()
    connection.close()

# Function to INSERT INTO time-series table for Grafana called 'passenger_count_epochtime_grafana'
def insert_timeseries_table(count):
    # Connect to the 'passenger_count_epochtime' table and read current counter value
    connection = mysql.connector.connect(**db_config)
    mycursor = connection.cursor()
    current_count_query = 'SELECT count FROM passenger_count_epochtime WHERE operator = %s'
    mycursor.execute(current_count_query, (operator_name, ))
    current_count = mycursor.fetchone()[0]
    eptime = int(time.time())

    # Connect to passenger_count_epochtime_grafana table and insert a new row
    # with current counter value and current epoch time
    insert_timeseries_table_query = 'INSERT INTO passenger_count_epochtime_grafana (operator, vehicle_id, count, epoch_time) VALUES (%s, %s, %s, %s)'
    mycursor.execute(insert_timeseries_table_query, (operator_name,vehicle_num,current_count,eptime))
    connection.commit()
    mycursor.close()
    connection.close()

def increment_counter(channel):
    global counter
    counter += 1
    print("Passenger Detected.")    
    update_counter(counter)
    insert_timeseries_table(counter)

def main():
    GPIO.setmode(GPIO.BCM)

    # Define GPIO pin as an input pin
    GPIO.setup(sensor_pin, GPIO.IN)

    # Identify the voltage drop in GPIO pin, when identiy call the increment_counter() function     
    GPIO.add_event_detect(sensor_pin, GPIO.FALLING, callback=increment_counter, bouncetime=200)  

    try:
        while True:
            ## GPIO.input(sensor_pin)             # To simulate sensor input change, only when there is no physical sensor
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()