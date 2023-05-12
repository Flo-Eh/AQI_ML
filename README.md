# AQI_ML

- First the data should be downloaded via the following link: 
https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india?select=station_hour.csv
- Data should be extracted in the Data folder
- station_hour.csv should be put in Code folder

- To create the Docker image:

```
docker build -t aqi
```
- To run the image:
```
docker run -d -p 8000:8000 aqi_ml
```
