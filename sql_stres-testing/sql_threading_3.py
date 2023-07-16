import concurrent.futures
import mysql.connector
import time

operator_name = 'ASTRA GmbH'
vehicle_num = 111222333

# Database connection settings
db_config = {
    'user': 'stressTestusr',
    'password': 'stressTestusr',
    'host': '192.168.1.129',
    'database': 'mydatabase'
}

def read_counter():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    select_query = "SELECT * FROM passenger_count_epochtime WHERE vehicle_id = 111222333"
    cursor.execute(select_query)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    connection.close()

def update_counter():
    connection = mysql.connector.connect(**db_config)
    mycursor = connection.cursor()
    update_counter_query = 'UPDATE passenger_count_epochtime SET count = count + 1 WHERE operator = %s AND vehicle_id = %s'
    eptime = int(time.time())
    mycursor.execute(update_counter_query, (eptime,operator_name,vehicle_num))
    connection.commit()
    mycursor.close()
    connection.close()

def read_updated_counter():
    connection = mysql.connector.connect(**db_config)
    mycursor = connection.cursor()
    current_count_query = 'SELECT count FROM passenger_count_epochtime WHERE operator = %s'
    mycursor.execute(current_count_query, (operator_name, ))
    mycursor.close()
    connection.close()

# Number of concurrent threads
num_threads = 1000

# Create a ThreadPoolExecutor with the desired number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit the tasks to the executor
    update_futures = [executor.submit(read_counter) for _ in range(num_threads)]
    select_futures = [executor.submit(update_counter) for _ in range(num_threads)]
    select_futures = [executor.submit(read_updated_counter) for _ in range(num_threads)]


    # Wait for all tasks to complete
    concurrent.futures.wait(update_futures + select_futures)