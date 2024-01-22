import pandas as pd
import matplotlib.pyplot as plt
import os

def get_sensor_id():
    # Retrieve sensor ID from environment variable, defaulting to 0 if not set
    return int(os.environ.get('SENSOR_ID', 0))

def get_excel_path():
    # Retrieve Excel file path from environment variable, defaulting to a default path if not set
    return os.environ.get('EXCEL_FILE_PATH', 'sensor_data_volume.xlsx')

def get_excel(file_path):
    excel_file = pd.read_excel(file_path)
    return excel_file

def create_chart(data, y_column, y_label, title, sensor_id=None, save_path=None):
    if sensor_id is not None:
        # Filter data for the specified sensor_id
        filtered_data = data[data['Sensor Id'] == sensor_id]
        title_suffix = f' (Sensor ID = {sensor_id})'
    else:
        filtered_data = data
        title_suffix = ''

    # Convert 'Timestamp' to datetime format using .loc
    filtered_data.loc[:, 'Timestamp'] = pd.to_datetime(filtered_data['Timestamp'])

    # Plotting
    plt.plot(filtered_data['Timestamp'], filtered_data[y_column], marker='o', linestyle='-', color='b')
    plt.xlabel('Timestamp')
    plt.ylabel(y_label)
    plt.title(f'{title}{title_suffix}')
    plt.xticks(rotation=45)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    plt.show()

def create_sensor_chart(data, sensor_id, output_path):
    create_chart(data, 'Humidity', 'Humidity', 'Humidity Trends Over Time', sensor_id, save_path=f"{output_path}/humidity_chart.png")
    create_chart(data, 'Temperature', 'Temperature', 'Temperature Trends Over Time', sensor_id, save_path=f"{output_path}/temperature_chart.png")
    create_chart(data, 'CO2', 'CO2', 'CO2 Trends Over Time', sensor_id, save_path=f"{output_path}/co2_chart.png")
    create_chart(data, 'NO2', 'NO2', 'NO2 Trends Over Time', sensor_id, save_path=f"{output_path}/no2_chart.png")

if __name__ == '__main__':
    sensor_id = get_sensor_id()
    excel_path = get_excel_path()
    excel_data = get_excel(excel_path)
    create_sensor_chart(excel_data, sensor_id, "/output")
