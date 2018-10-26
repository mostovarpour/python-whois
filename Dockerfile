FROM python:2

EXPOSE 8080

WORKDIR /app

run pip install pymysql

COPY . .

# ARG mysql
# CMD python main.py $ENV1
ENTRYPOINT [ "python", "main.py" ]