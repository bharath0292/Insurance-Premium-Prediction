from typing import Optional
import uvicorn
from fastapi import FastAPI,Response
import json
from starlette.applications import Starlette
from fastapi.responses import ORJSONResponse

#extra imports
import numpy as np
import pickle
import pandas as pd


from sklearn.preprocessing import LabelEncoder
from typing import Dict
import joblib

from sklearn.preprocessing import MinMaxScaler


from application_logging import logger
from data_preprocessing import preprocessing
from file_operations import file_methods


from fastapi import Request
from fastapi.responses import HTMLResponse,JSONResponse

from fastapi.staticfiles import StaticFiles



# from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from prediction_Validation_Insertion import pred_validation # need to fix
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
#  import flask_monitoringdashboard as dashboard
from predictFromModel import prediction # need to fix
#import json
#import request
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware



# For Cross Origin
app = FastAPI(debug = True)

app.mount("/static", StaticFiles(directory="static"), name="static")


templats = Jinja2Templates(directory= "templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
     )


# For HTML integreation
# For HTML integreation
@app.get("/",response_class=HTMLResponse)
async def index(request: Request):
	return templats.TemplateResponse('index.html',{"request": request})



@app.get("/admin",response_class=HTMLResponse)
async def index(request: Request):
	return templats.TemplateResponse('admin.html',{"request": request})






# simple implementaion of predict route
@app.post("/predictmodel")
def predictRoute(json_data: Dict,response_class=JSONResponse):
    try:

        data = [json_data]
        data = pd.DataFrame.from_dict(data)
        label_encoder = LabelEncoder()
        data['sex'] = label_encoder.fit_transform(data['sex'])
        data['smoker'] = label_encoder.fit_transform(data['smoker'])
        data['region'] = label_encoder.fit_transform(data['region'])

        # data = pd.get_dummies(data, columns=['region'], drop_first=True)

        # scaler = MinMaxScaler(feature_range=(0, 1))
        # data = scaler.fit_transform(data)
        # data = pd.DataFrame(data)

        model_path = './modeljson/RandomForest'
        with open('./modeljson/RandomForest' + '/RandomForest.sav', 'rb') as f:
            model = joblib.load(f)

        result = model.predict(data)
        return {"result":str(result[0])}

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

   



@app.post("/predict")
def predictRouteClient(json_data: Dict):
     try:
        if json_data.get('folderPath') is not None:
             path = json_data.get('folderPath')

             pred_val = pred_validation(path) #object initialization

             pred_val.prediction_validation() #calling the prediction_validation function

             pred = prediction(path) #object initialization

             # predicting for dataset present in database
             path = pred.predictionFromModel()
             #return Response({'response':"Prediction File created at %s!!!" % path})
             return {'response':"Prediction File created at %s!!!" % path}

     except ValueError:
         return Response("Error Occurred! %s" %ValueError)
     except KeyError:
         return Response("Error Occurred! %s" %KeyError)
     except Exception as e:
         return Response("Error Occurred! %s" %e)






