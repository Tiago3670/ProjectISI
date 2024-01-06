import pika
import json
import time
import numpy as np
from datetime import datetime, timedelta
import os

def simulate_values():
        sensor_id = os.getenv("sensorID")

        sensorInfo = {
            "sensorID": sensor_id,
            "co2": 0,
            "no2": 0,
            "humidity": 0,
            "temperature": 0,
            "lastReadDate": ""
        }
        # Conectar ao servidor RabbitMQ
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2', 5672, '/',credentials))
        channel = connection.channel()
        
        channel = connection.channel()
        # Declare a queue named 'values_queue'
        channel.queue_delete(queue='values_queue')
        channel.queue_declare(queue='values_queue', durable=True)

        while True:
            # Generate co2 levels
            co2_levels = np.random.normal(350, 50)
            co2_levels = np.clip(co2_levels, 278, 4500)
            rounded_co2_levels = round(co2_levels, 1)
            sensorInfo["co2"] = rounded_co2_levels

            # Generate no2 levels
            no2_levels = np.random.normal(50, 10)
            no2_levels = np.clip(no2_levels, 0, 200)
            rounded_no2_levels = round(no2_levels, 1)
            sensorInfo["no2"] = rounded_no2_levels

            # Generate temperature levels
            temperature_levels = np.random.normal(15, 5)
            temperature_levels = np.clip(temperature_levels, -40, 50)
            rounded_temperature_levels = round(temperature_levels, 1)
            sensorInfo["temperature"] = rounded_temperature_levels

            # Generate humidity levels
            humidity_levels = np.random.normal(70, 10)
            humidity_levels = np.clip(humidity_levels, 0, 100)
            rounded_humidity_levels = round(humidity_levels, 1)
            sensorInfo["humidity"] = rounded_humidity_levels

            # Get the date and time
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sensorInfo["lastReadDate"] = dt_string

            print(sensorInfo)
            # Convert the values to JSON
            message_body = json.dumps(sensorInfo)

            # Publish the message to the 'values_queue' queue
            channel.basic_publish(exchange='', routing_key='values_queue', body=message_body)

            print("Sent values: {values_data}")

            # Simulate a delay (adjust as needed)
            time.sleep(10)

if __name__ == "__main__":
    
    simulate_values()
