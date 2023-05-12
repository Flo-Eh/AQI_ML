# AQI_ML
## This project allow to predict the AQI of a selected station
### Preprocess 
- First the data should be downloaded via the following link: 
https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india?select=station_hour.csv
- Data should be extracted in the Data folder
- station_hour.csv should be put in Code folder
- there is one requirements.txt at the root to dockerise and another one in the data folder to be able to run the notebook
### Creating and runnin the docker image
- To create the Docker image:

```
docker build -t aqi
```
- To run the image:
```
docker run -d -p 8000:8000 aqi
```
### Using the API
- go to [http:](http://localhost:8000/docs)

- To get the prediction, choose a station Id amoung ('AP001', 'AP005', 'AS001', 'BR005', 'BR006', 'BR007', 'BR008','BR009', 'BR010', 'CH001', 'DL001', 'DL002', 'DL003', 'DL004','DL005', 'DL006', 'DL007', 'DL008', 'DL009', 'DL010', 'DL011','DL012', 'DL013', 'DL014', 'DL015', 'DL016', 'DL017', 'DL018','DL019', 'DL020', 'DL021', 'DL022', 'DL023', 'DL024', 'DL025','DL026', 'DL027', 'DL028', 'DL029', 'DL030', 'DL031', 'DL032','DL033', 'DL034', 'DL035', 'DL036', 'DL037', 'DL038', 'GJ001','HR011', 'HR012', 'HR013', 'HR014', 'JH001', 'KA002', 'KA003','KA004', 'KA005', 'KA006', 'KA007', 'KA008', 'KA009', 'KA010','KA011', 'KL002', 'KL004', 'KL007', 'KL008', 'MH005', 'MH006','MH007', 'MH008', 'MH009', 'MH010', 'MH011', 'MH012', 'MH013','MH014', 'ML001', 'MP001', 'MZ001', 'OD001', 'OD002', 'PB001','RJ004', 'RJ005', 'RJ006', 'TG001', 'TG002', 'TG003', 'TG004','TG005', 'TG006', 'TN001', 'TN002', 'TN003', 'TN004', 'TN005','UP012', 'UP013', 'UP014', 'UP015', 'UP016', 'WB007', 'WB008','WB009', 'WB010', 'WB011', 'WB012', 'WB013')

- The result will be a dictionnary: {Datetime:[:],AQI:[:],AQI_Bucket:[:]}
