FROM python:3

RUN mkdir -p /app

WORKDIR /app

COPY flask-air-monitor/requirements.txt ./

RUN pip install -r requirements.txt

COPY flask-air-monitor/ .

EXPOSE 7071

CMD [ "flask", "run", "--port", "7071", "--host", "0.0.0.0" ] 
