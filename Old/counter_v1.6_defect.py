###################################################################################################
##                              Raspberry Pi Passenger Counter                                  ##
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
def update_counter(sensor_pin):
    connection = mysql.connector.connect(**db_config)
    mycursor = connection.cursor()
    update_counter_query = 'UPDATE passenger_count_epochtime SET count = count + 1, epoch_time = %s WHERE operator = %s AND vehicle_id = %s'
    eptime = int(time.time())
    mycursor.execute(update_counter_query, (eptime,operator_name,vehicle_num))
    connection.commit()
    mycursor.close()
    connection.close()

# Function to INSERT INTO time-series table for Grafana called 'passenger_count_epochtime_grafana'
def insert_timeseries_table(sensor_pin):
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

def main():
    # Use the pin numbering scheme BCM (Broadcom)
    GPIO.setmode(GPIO.BCM)

    # Define GPIO pin as an input pin
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
    GPIO.setup(sensor_pin, GPIO.IN)

    # Identify the voltage drop in GPIO pin
    # When detects, run two callback functions sequentally using 2nd thread, in parallel to main function
    # https://tieske.github.io/rpi-gpio/modules/GPIO.html
    # Two callback functions will run sequentially
    GPIO.add_event_detect(sensor_pin, GPIO.FALLING)
    GPIO.add_event_callback(sensor_pin, update_counter)
    GPIO.add_event_callback(sensor_pin, insert_timeseries_table)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()