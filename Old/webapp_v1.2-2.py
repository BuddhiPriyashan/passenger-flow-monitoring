rom flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def query_database():
    # Establish a new connection and cursor for each request
    mydb = mysql.connector.connect(
        host="192.168.1.129",
        user="webappusr",
        password="webappusr",
        database="passenger_flow_counts"
    )
    mycursor = mydb.cursor()

    if mycursor:
        try:
            # Define the select query
            select_query = "SELECT * FROM passenger_count_epochtime WHERE operator = %s AND vehicle_id = %s"

            # Set the corresponding operator value
            record_id = 'ASTRA GmbH'
            operator_vehicle_id = '111222333'

            # Execute the select query
            mycursor.execute(select_query, (record_id, operator_vehicle_id))

            # Fetch the query result
            query_result = mycursor.fetchall()

            # Close the cursor and the database connection
            mycursor.close()
            mydb.close()

            # Pass the query result to the template for rendering
            return render_template('index.html', result=query_result)

        except mysql.connector.Error as error:
            print("Error executing SQL query:", error)
            mycursor.close()
            mydb.close()
            return "Error executing SQL query"

    else:
        return "Error connecting to the database"

if __name__ == '__main__':
    # Access app from all IP addresses
    app.run(host='0.0.0.0')