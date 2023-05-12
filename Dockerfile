FROM python:3.10-slim

RUN apt-get update && apt-get install python3-pip -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

COPY ./Code/MLapi.py .

COPY ./Data/station_hour.csv ./station_hour.csv

COPY ./Code/SVR_model_best_param.sav ./SVR_model_best_param.sav

CMD ["uvicorn","MLapi:app","--host","0.0.0.0","--port","8000"]