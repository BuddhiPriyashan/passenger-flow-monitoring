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

# [Table] MySQL statements:
CREATE TABLE passenger_count_epochtime (operator VARCHAR(255), vehicle_id VARCHAR(255), count INT, epoch_time INT);
INSERT INTO passenger_count_epochtime ( operator, vehicle_id, count, epoch_time) VALUES ( 'Operator-1', '111222333', '0', '1689192443' );
UPDATE passenger_count_epochtime SET operator = 'ASTRA GmbH' WHERE operator = 'Operator-1';
# [User] MySQL statements:
CREATE USER 'stressTestusr'@'192.168.1.129';
GRANT ALL PRIVILEGES ON *.* TO 'stressTestusr'@'192.168.1.129' WITH GRANT OPTION;
SET PASSWORD FOR 'stressTestusr'@'192.168.1.129' = 'stressTestusr';

#A Grafana Query
SELECT count AS value, epoch_time AS time FROM passenger_flow_counts.passenger_count_epochtime WHERE operator='ASTRA GmbH';



# Project Name

Short description or tagline for your project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Provide an overview and background of your project. Explain its purpose and what problems it aims to solve.

## Features

List the key features and functionalities of your project.

## Installation

Provide instructions on how to install and set up your project. Include any dependencies or prerequisites.

## Usage

Demonstrate how to use your project with code examples or step-by-step guides. Include any relevant configurations or settings.

## Contributing

Outline guidelines for contributing to your project, including information on how others can contribute, report issues, or submit pull requests.

## License

Specify the license under which your project is distributed.

## Acknowledgements

Give credit to any individuals or resources that have inspired or assisted your project.

## Contact

Provide contact information or links to reach out to you for support or inquiries.
