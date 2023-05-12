import uvicorn 
from fastapi import FastAPI, Header
from pydantic import BaseModel
import pickle 
from sklearn.preprocessing import LabelEncoder
import pandas as pd 
import numpy as np 

def get_AQI_bucket(x):
    if x <= 50:
        return "Good"
    elif x <= 100:
        return "Satisfactory"
    elif x <= 200:
        return "Moderate"
    elif x <= 300:
        return "Poor"
    elif x <= 400:
        return "Very Poor"
    elif x > 400:
        return "Severe"
    else:
        return np.NaN

def preprocess(df):
    df.drop(['Xylene','NH3'],axis=1, inplace=True)    
    columns_list = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'CO','SO2', 'O3', 'Benzene', 'Toluene', 'AQI']
    for columns in columns_list:
        df[columns] = df[columns].fillna(df[columns].median())
        
    df['AQI_Bucket'] =  df['AQI'].map(lambda x: get_AQI_bucket(x))
    le=LabelEncoder()   
    df['AQI_Bucket']=le.fit_transform(df['AQI_Bucket'].astype(str))
    df.set_index('Datetime', inplace = True)
    df.drop(['StationId'],axis=1,inplace=True) 
    Train =df.head(round(len(df)*80/100))
    Test = df.tail(len(df)-round(len(df)*80/100))

    X_train, X_test = Train.drop(['AQI'],axis=1), Test.drop(['AQI'],axis=1)
    y_train, y_test = Train['AQI'], Test['AQI']
    

    return X_test, y_test


app = FastAPI()

class station(BaseModel):
    StationName: str

with open('SVR_model_best_param.sav','rb') as f: 
    model = pickle.load(f)


@app.post('/prediction/station')
""" Predict emission for a choosen station\n
Station list:['AP001', 'AP005', 'AS001', 'BR005', 'BR006', 'BR007', 'BR008',
       'BR009', 'BR010', 'CH001', 'DL001', 'DL002', 'DL003', 'DL004',
       'DL005', 'DL006', 'DL007', 'DL008', 'DL009', 'DL010', 'DL011',
       'DL012', 'DL013', 'DL014', 'DL015', 'DL016', 'DL017', 'DL018',
       'DL019', 'DL020', 'DL021', 'DL022', 'DL023', 'DL024', 'DL025',
       'DL026', 'DL027', 'DL028', 'DL029', 'DL030', 'DL031', 'DL032',
       'DL033', 'DL034', 'DL035', 'DL036', 'DL037', 'DL038', 'GJ001',
       'HR011', 'HR012', 'HR013', 'HR014', 'JH001', 'KA002', 'KA003',
       'KA004', 'KA005', 'KA006', 'KA007', 'KA008', 'KA009', 'KA010',
       'KA011', 'KL002', 'KL004', 'KL007', 'KL008', 'MH005', 'MH006',
       'MH007', 'MH008', 'MH009', 'MH010', 'MH011', 'MH012', 'MH013',
       'MH014', 'ML001', 'MP001', 'MZ001', 'OD001', 'OD002', 'PB001',
       'RJ004', 'RJ005', 'RJ006', 'TG001', 'TG002', 'TG003', 'TG004',
       'TG005', 'TG006', 'TN001', 'TN002', 'TN003', 'TN004', 'TN005',
       'UP012', 'UP013', 'UP014', 'UP015', 'UP016', 'WB007', 'WB008',
       'WB009', 'WB010', 'WB011', 'WB012', 'WB013'] """
def prediction(item:station):
    #open file, preprocess and split data
    df = pd.read_csv('station_hour.csv')
    df = df[df['StationId']==item.StationName]
    X_test, y_test = preprocess(df)
      
    #prediction
    y_pred = list(model.predict(X_test))
    #get AQI Bucket
    bucket=[]
    for items in y_pred:
        a = get_AQI_bucket(items)
        bucket.append(a)

    return {'DateTime': list(y_test.index),
            'prediction':y_pred,
            'AQI bucket':bucket }




