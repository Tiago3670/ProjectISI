FROM python:3.12-slim

WORKDIR /app

ADD receaver.py .

RUN pip install pika pandas openpyxl 

CMD [ "python", "./receaver.py" ]
