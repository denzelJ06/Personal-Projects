import numpy as np
import pandas as pd

#Loading Data
data = pd.read_csv("Projects/Credit_Card_Fraud/data/fraudTest.csv")

def haversine_np(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

#data.info()

#Adjusting Column Names
data = data.rename(columns = {
    "Unnamed: 0":"Trans_no",
    "trans_date_trans_time": "trans_Date_&_Time"
    })

columns_drop = [
    "first",    #do not require the names for flagging fraud
    "last",
    "trans_num", #already have a column that is cleaner which is Trans_no
    "street",    #already have zip, lat and long for position
    "unix_time",  #redundant column as there is already trans_Date_&_Time
    "gender"
    ]

data = data.drop(columns=columns_drop)

#Converting data types of columns
data["trans_Date_&_Time"] = pd.to_datetime(data["trans_Date_&_Time"],format="%Y-%m-%d %H:%M:%S")
data['day_of_week'] = data['trans_Date_&_Time'].dt.dayofweek
data["cc_num"] = (data["cc_num"]).astype(str)
data["dob"] = pd.to_datetime(data["dob"],format="%Y-%m-%d") # changing date of birth to age during transaction
data['age'] = (data['trans_Date_&_Time'] - data['dob']).dt.days // 365
data = data.drop(columns=['dob'])
data['merchant'] = data['merchant'].str.replace('fraud_', '', regex=False)
data['distance_km'] = haversine_np(data['lat'], data['long'], data['merch_lat'], data['merch_long'])
data = data.drop(columns=['lat', 'long', 'merch_lat', 'merch_long'])    #used AI to create subroutine to change lat and long to distance
data["hour"] = data['trans_Date_&_Time'].dt.hour

#data.info()
#print(data[data["is_fraud"]==1])
#print(data.nunique())
#print(data.isnull().sum())

# Save the cleaned DataFrame to a new CSV file
data.to_csv("Projects/Credit_Card_Fraud/data/cleaned_fraudTest.csv", index=False)