try:
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    import json
    import boto3
    import os
    from datetime import datetime
    from io import StringIO # python 3.x
except Exception as e:
    print(e)
    
class MongoDB():
    def __init__(self,dBName=None,CollectionName=None):
        self.dBName=dBName
        self.CollectionName=CollectionName
        
        self.client=MongoClient("localhost")
        self.DB=self.client[self.dBName]
        self.collection=self.DB[self.CollectionName]
        
        
    def insertData(self,bucket_name="insurancePrem",object_key="inspremtrain.csv"):
        """
        parameters: Bucket_name,Object_key(csv from s3)
        return: None
        """
        try:
            access_key='AKIATXABL6T7RQNSKKSE'
            secret_key='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'
            client=boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_key)



            #buck_name="insurancedataset"
            #object_key="inspremtrain.csv"


            csv_obj=client.get_object(Bucket=bucket_name,Key=object_key)
            body=csv_obj["Body"]
            csv_string=body.read().decode('utf-8')
            df=pd.read_csv(StringIO(csv_string))
        
            #convert dataframe to dictionary
            data=df.to_dict('records')
            self.collection.insert_many(data, ordered=False)


            #print("All data inserted to mongoDB")

            print("2: Check for data retrieval")
            cursor = self.collection.find({})

            complete_data=[]
            for d in cursor:
                complete_data.append(d)
            
            #Step 3: Saving the data retrieved from the mongodb into csv .
            df_actual = pd.json_normalize(complete_data)
            timestamp_string = "HealthPrem"+str(datetime.now().strftime('_%d%m%Y_%H%M%S'))
            path_store = os.path.join(os.getcwd(), "Training_Batch_Files/"+timestamp_string+".csv")
            df_actual.to_csv(path_store)
            return path_store
        except:
            print("Check for the error")


    def retreiveData(self):
        """
        :parameter: None

        :return: path of CSV file thats used to store the data.
        """
        try:
            access_key = 'AKIATXABL6T7RQNSKKSE'
            secret_key = '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'
            client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

            bucket_name="insurancedataset"
            object_key="inspremtrain.csv"
            client.get_object(Bucket=bucket_name, Key=object_key)
            cursor = self.collection.find({})

            complete_data = []
            for d in cursor:
                complete_data.append(d)

            # Step 3: Saving the data retrieved from the mongodb into csv .
            df_actual = pd.json_normalize(complete_data)
            df_actual=df_actual.drop(columns=["_id"])
            random_value=r"Training_Batch_Files\HealthPrem_26092020_131535.csv"
            path_store =r"./Training_Batch_Files/HealthPrem_26092020_131535.csv"
            ret_path=r"./Training_Batch_Files"
            df_actual.to_csv(path_store)
            return ret_path




        except:
            print("There is an error in retrieving data")




        
        
        


#buck_name="insurancedataset"
#object_key="inspremtrain.csv"
#
# dbname=input("enter dbname of S3 bucket")
# collection=input("enter the object key in S3 dataset")
# mongoDB= MongoDB(dBName="insurancePrem",CollectionName="DataPremium")
# mongoDB.insertData(dbname,collection)

    
    