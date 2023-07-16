from flask import Flask, render_template
import mysql.connector

# [Flask Doc] https://flask.palletsprojects.com/en/2.3.x/
app = Flask(__name__)
# Route decorator for root URL
@app.route('/')

def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
# Route decorator for root URL when a POST request is sent to root URL
# POST request is created when user press the 'RUN' button


def select_counter():
    operator_name = 'ASTRA GmbH'
    vehicle_num = 111222333
    db_config = {
        'host' : '192.168.1.129',
        'user' : 'webappusr',
        'password' : 'webappusr',
        'database' : 'passenger_flow_counts'
    }

    connection = mysql.connector.connect(**db_config)
    mycursor = connection.cursor()
    select_query = "SELECT * FROM passenger_count_epochtime WHERE operator = %s AND vehicle_id = %s"
    mycursor.execute(select_query, (operator_name, vehicle_num))
    query_result = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('index.html', result=query_result)

if __name__ == '__main__':
    # Access app from all IP addresses
    app.run(host='0.0.0.0')