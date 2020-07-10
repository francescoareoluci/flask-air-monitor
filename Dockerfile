FROM python:3.6-slim

RUN mkdir -p /app

WORKDIR /app

COPY flask-air-monitor/requirements.txt ./

RUN pip install -r requirements.txt

COPY flask-air-monitor/ .

RUN python3 resources/pull_sensor_data/get_sensors_data.py resources/samples/

EXPOSE 7071

CMD [ "flask", "run", "--port", "7071", "--host", "0.0.0.0" ] 
