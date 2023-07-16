$ sudo docker build -t iot/webapp:1.6 .
Sending build context to Docker daemon  11.26kB
Step 1/7 : FROM python:3.10.6
 ---> 93aefc89ba9e
Step 2/7 : WORKDIR /query_mysql
 ---> Using cache
 ---> a5cdf3c44514
Step 3/7 : COPY . /query_mysql 
 ---> 6be4c0e139de
Step 4/7 : RUN pip install mysql-connector-python
 ---> Running in 25317304152f
Collecting mysql-connector-python
.......
Step 5/7 : RUN pip install Flask
 ---> Running in 44b666511918
Collecting Flask
......
Step 6/7 : EXPOSE 5000
 ---> Running in d4b2e9937040
Removing intermediate container d4b2e9937040
 ---> 8f0b8478cf12
Step 7/7 : CMD ["python", "webapp_v1.3.py", "--host", "0.0.0.0"]
 ---> Running in 5e5da0a9c221
Removing intermediate container 5e5da0a9c221
 ---> 92af2baf62e6
Successfully built 92af2baf62e6
Successfully tagged iot/webapp:1.6