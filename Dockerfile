FROM python:2

EXPOSE 8080

WORKDIR /app

run pip install pymysql

COPY . .

CMD [ "python", "./main.py" ]