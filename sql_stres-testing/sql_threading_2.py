import concurrent.futures
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
num_threads = 1000

# Create a ThreadPoolExecutor with the desired number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit the tasks to the executor
    update_futures = [executor.submit(perform_update) for _ in range(num_threads)]
    select_futures = [executor.submit(perform_select) for _ in range(num_threads)]

    # Wait for all tasks to complete
    concurrent.futures.wait(update_futures + select_futures)