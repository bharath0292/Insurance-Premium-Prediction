import pandas as pd
import json
import boto3
import sys
from io import StringIO # python 3.x

#data_frame = pd.read_csv('data/HealthPrem_26092020_131534.csv')

df=pd.read_csv('data/HealthPrem_26092020_131534.csv')
#csv_obj=client.get_object(Bucket=bucket_name,Key=object_key)

print('Hello All good till loading the data file')

#body=csv_obj["Body"]
#csv_string=body.read().decode('utf-8')
#df=pd.read_csv(StringIO(csv_string))

data=df.to_dict('records')


#################################

from pymongo import MongoClient
MONGO_URL = sys.argv[1]

myclient = MongoClient(MONGO_URL)
print(myclient.list_database_names())
db = myclient.get_database('insurance-premium-prediction')
print(db.list_collection_names())

mydb = myclient["insurance-premium-prediction"]
mycol = mydb["HealthPrem"]
mycol.drop()


mycol.insert_many(data)
print('The Data is loaded to CLOUD MONGO DB')
