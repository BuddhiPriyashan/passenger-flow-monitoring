import mysql.connector
import RPi.GPIO as GPIO
import time

sensor_pin = 2
counter = 0

def save_to_database(count):
    print("Started save_to_database method")
    # Establish a new connection and cursor for each request
    mydb = mysql.connector.connect(
        host="192.168.1.129",
        user="piusr",
        password="piusr",
        database="passenger_flow_counts"
    )
    mycursor = mydb.cursor()

    # Define the update query
    update_query = 'UPDATE passenger_count_epochtime SET count = count + 1, epoch_time = %s WHERE operator = %s AND vehicle_id = %s'
    # Set the new value and the corresponding ID
    increment = 1
    eptime = int(time.time())
    record_id = 'ASTRA GmbH'
    vehicle_id = 111222333
    # Execute the update query
    mycursor.execute(update_query, (eptime, record_id, vehicle_id))
    # Commit the changes to the database
    mydb.commit()

    # Define the insert query
    insert_query = 'INSERT INTO passenger_count_epochtime_grafana (operator, vehicle_id, epoch_time, count) VALUES (%s, %s, %s, %s)'
    # Execute the insert query
    mycursor.execute(insert_query, (record_id, vehicle_id, eptime, count))
    # Commit the changes to the database
    mydb.commit()

    # Close the cursor and the database connection
    mycursor.close()
    mydb.close()

def increment_counter(channel):
    print("Increment counter")
    global counter
    if counter == 10:
        print("Counter:", counter)
        save_to_database(counter)
        counter = 0
    else:
        counter += 1

    print("Counter:", counter)
    save_to_database(counter)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_pin, GPIO.IN)
    GPIO.add_event_detect(sensor_pin, GPIO.FALLING, callback=increment_counter, bouncetime=200)

    try:
        while True:
            # Simulate sensor input change every 2 seconds
            GPIO.input(sensor_pin)  # Read input status (not necessary in this case)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()