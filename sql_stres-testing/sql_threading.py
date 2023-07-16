import threading
import mysql.connector
import time

# Database connection settings
db_config = {
    'user': 'stressTestusr',
    'password': 'stressTestusr',
    'host': '192.168.1.129',
    'database': 'mydatabase'
}

# Function to perform update queries
def perform_update():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    update_query = 'UPDATE passenger_count_epochtime SET count = count + 1, epoch_time = %s WHERE operator = %s AND vehicle_id = %s'
    # Set the new value and the corresponding ID
    eptime = int(time.time())
    record_id = 'ASTRA GmbH'
    vehicle_id = 111222333
    # Execute the update query
    cursor.execute(update_query, (eptime, record_id, vehicle_id))
    # Commit the changes to the database
    connection.commit()
    cursor.close()
    connection.close()

def perform_insert():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    # Define the insert query
    insert_query = 'INSERT INTO passenger_count_epochtime_grafana (operator, vehicle_id, epoch_time, count) VALUES (%s, %s, %s, %s)'
    # Execute the insert query
    eptime = int(time.time())
    record_id = 'ASTRA GmbH'
    vehicle_id = 111222333
    count = 33
    cursor.execute(insert_query, (record_id, vehicle_id, eptime, count))
    # Commit the changes to the database
    connection.commit()


# Function to perform select queries
def perform_select():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    select_query = "SELECT * FROM passenger_count_epochtime_3 WHERE vehicle_id = 111222333"
    cursor.execute(select_query)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    connection.close()

# Number of concurrent threads
num_threads = 500

# Create and start the threads
threads = []
for _ in range(num_threads):
    update_thread = threading.Thread(target=perform_update)
    select_thread = threading.Thread(target=perform_select)
    threads.append(update_thread)
    threads.append(select_thread)
    update_thread.start()
    select_thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()