FROM python:2

ADD main.py /

run yum update && yum install python-pip
run pip install pymysql

CMD [ "python", "./main.py" ]