import pika
import pandas as pd
from datetime import datetime
import json
EXCEL_FILE_PATH = '/app/sensor_data_volume.xlsx'

def callback(ch, method, properties, body):
    print(f"Recebeu uma mensagem: {body}")
    data = json.loads(body.decode('utf-8'))

    # Extract values into variables
    sensor_id = data['sensorID']
    co2 = data['co2']
    no2 = data['no2']
    humidity = data['humidity']
    temperature = data['temperature']
    last_read_date = data['lastReadDate']
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {'Timestamp': timestamp, 'Sensor Id': sensor_id, 'CO2': co2, 'NO2': no2, 'Humidity': humidity, 'Temperature': temperature, 'Last Read Date': last_read_date}
    df = pd.DataFrame([data])

    try:
        existing_data = pd.read_excel(EXCEL_FILE_PATH)
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_excel(EXCEL_FILE_PATH, index=False)
def receive_messages():
    # Conectar ao servidor RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2', 5672, '/',credentials))
    channel = connection.channel()

    channel.queue_delete(queue='values_queue')
    channel.queue_declare(queue='values_queue', durable=True)

    channel.basic_consume(queue='values_queue', on_message_callback=callback, auto_ack=True)

    print('Aguardando mensagens. Para sair, pressione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    receive_messages()
