FROM python:3.10.6

WORKDIR /query_mysql

COPY . /query_mysql

RUN pip install mysql-connector-python
RUN pip install Flask

EXPOSE 5000

CMD ["python", "webapp_v1.3.py", "--host", "0.0.0.0"]