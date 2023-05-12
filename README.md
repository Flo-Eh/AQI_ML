# AQI_ML

First the data should be downloaded via the following link and extracted into the data folder:
https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india?select=station_hour.csv

To create the Docker image:

```
docker build -t aqi
```
To run the image:
```
docker run -d -p 8000:8000 aqi_ml
```
