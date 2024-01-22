FROM python:3.12-slim

ADD sensor.py .

ENV sensorID=0
    
RUN pip install pika numpy 

CMD [ "python", "./sensor.py" ]
