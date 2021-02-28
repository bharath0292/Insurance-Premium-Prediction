import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.impute import KNNImputer

class Preprocessor:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object


    def separate_label_feature(self, data, label_column_name):

        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X=data.drop(labels=label_column_name,axis=1) # drop the columns specified and separate the feature columns
            self.Y=data[label_column_name] # Filter the Label columns
            self.logger_object.log(self.file_object, 'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X,self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()



    def is_null_present(self,data):

        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        try:
            self.null_counts=data.isna().sum() # check for the count of null values per column
            for i in self.null_counts:
                if i>0:
                    self.null_present=True
                    break
            if(self.null_present): # write the logs to see which columns have null values
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            self.logger_object.log(self.file_object,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()



    def encodeCategoricalValues(self, data):


        # We can map the categorical values like below:
        # Encode Sex column
        data['sex'] = data['sex'].map({'female': 0, 'male': 1})

        # Let's encode the smoker column
        data['smoker'] = data['smoker'].map({'no': 0, 'yes': 1})

        # Lets encode the region column by dummies
        data = pd.get_dummies(data, columns=['region'],drop_first=True)
        data = data

        return data


    def normalizeValues(self,Y):
        self.raw_data = Y
        self.raw_data = np.log10(self.raw_data)
        self.raw_data = self.raw_data.to_frame()
        return self.raw_data




    def encodeCategoricalValuesPrediction(self,data):

        # We can map the categorical values like below:
        data['sex'] = data['sex'].map({'female': 0, 'male': 1})

        # Let's encode the smoker column
        data['smoker'] = data['smoker'].map({'no': 0, 'yes': 1})

        # we will use get dummies for 'referral_source'
        #data = pd.get_dummies(data, columns=['region'],drop_first=True)

        # Dropping region column
        data = data.drop(['region'], axis=1)

        cols = list(data.columns)
        

        return cols,data



    def impute_missing_values(self, data):
        """
                                        Method Name: impute_missing_values
                                        Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
                                        Output: A Dataframe which has all the missing values imputed.
                                        On Failure: Raise Exception
                     """
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data= data
        try:
            imputer=KNNImputer(n_neighbors=4, weights='uniform',missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data) # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            # rounding the value because KNNimputer returns value between 0 and 1, but we need either 0 or 1
            self.new_data=pd.DataFrame(data=np.round(self.new_array), columns=self.data.columns)
            self.logger_object.log(self.file_object, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()








