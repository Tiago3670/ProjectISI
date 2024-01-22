FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pandas matplotlib openpyxl
RUN mkdir /output

ENV EXCEL_FILE_PATH sensor_data_volume.xlsx
ENV sensorID=0

CMD ["python", "./main.py"]