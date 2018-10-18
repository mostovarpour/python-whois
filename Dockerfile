FROM python:2

ADD main.py /
add TheSocket.py /
add os.py /

run yum install python-pip
run pip install mysql-python

CMD [ "python", "./main.py" ]