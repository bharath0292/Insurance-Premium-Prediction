from typing import Optional
import uvicorn

import json

import pymongo
from pymongo import MongoClient
import pandas as pd
import json

import os
from io import StringIO # python 3.x




#extra imports
import numpy as np
import pickle
import pandas as pd


from sklearn.preprocessing import LabelEncoder
from typing import Dict
import joblib
import mongotry

from sklearn.preprocessing import MinMaxScaler


from application_logging import logger
from data_preprocessing import preprocessing
from file_operations import file_methods






# from pydantic import BaseModel

from prediction_Validation_Insertion import pred_validation # need to fix
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
#  import flask_monitoringdashboard as dashboard
from predictFromModel import prediction # need to fix
#import json
#import request
from typing import Dict
try:
    trainModelObj = trainModel()  # object initialization
    trainModelObj.trainingModel()


except ValueError:

    print("Error Occurred! %s" % ValueError)

except KeyError:

    print("Error Occurred! %s" % KeyError)

except Exception as e:

    print('Error Occurred! '+str(e))
print("Training successfull!!")
