import uvicorn 
from fastapi import FastAPI
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
def prediction(item:station):
    #open file, preprocess and split data
    df = pd.read_csv('station_hour.csv')
    df = df[df['StationId']==item.StationName]
    X_test, y_test = preprocess(df)
      
    #prediction
    y_pred = list(model.predict(X_test))
    
    bucket=[]
    for items in y_pred:
        a = get_AQI_bucket(items)
        bucket.append(a)

    return {'DateTime': list(y_test.index),
            'prediction':y_pred,
            'AQI bucket':bucket }




