# Doing the necessary imports
from sklearn.model_selection import train_test_split
from data_ingestion import data_loader
from data_preprocessing import preprocessing
from data_preprocessing import clustering
from best_model_finder import tuner
from file_operations import file_methods
from application_logging import logger
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#Creating the common Logging object


class trainModel:

    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("./Training_Logs/ModelTrainingLog.txt", 'a+')
    def trainingModel(self):
        # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Training')
        try:
            # Getting the data from the source
            print()
            print()
            print("Entered Model Training")
            print()
            print()
            data_getter=data_loader.Data_Getter(self.file_object,self.log_writer)
            data=data_getter.get_data()


            """doing the data preprocessing"""
            print("----------------")
            print("Preprocessing")

            preprocessor=preprocessing.Preprocessor(self.file_object,self.log_writer)


            # get encoded values for categorical data

            data['sex'] = data['sex'].map({'female': 0, 'male': 1})
            data['smoker'] = data['smoker'].map({'no' : 0, 'yes' : 1})

            # Dropping region column
            data = data.drop(['region'], axis=1)
            #data = data.drop(['smoker'], axis=1)

            cols = list(data.columns)
            cols.remove('expenses')
            #data = pd.concat([pd.get_dummies(data.region), data.iloc[:,[1,2,3,4,6]]] , axis = 1)


            #min max scaling
            # transofrm data
            #scaler = MinMaxScaler(feature_range=(0, 1))
            #data = scaler.fit_transform(data)
            
            #converting back to dataframe
            #data = pd.DataFrame(data)

            # create separate features and labels
            X,Y=preprocessor.separate_label_feature(data,label_column_name='expenses')


            Y = preprocessor.normalizeValues(Y);

            # check if missing values are present in the dataset
            is_null_present=preprocessor.is_null_present(X)


            # if missing values are there, replace them appropriately.
            if(is_null_present):
                X=preprocessor.impute_missing_values(X) # missing value imputation



            """ Applying the clustering approach"""
            print()
            print("---------------")
            print("CLustering Process")

            kmeans=clustering.KMeansClustering(self.file_object,self.log_writer) # object initialization.
            number_of_clusters=kmeans.elbow_plot(X)  #  using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X=kmeans.create_clusters(X,number_of_clusters)

            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels']=Y

            # getting the unique clusters from our dataset
            list_of_clusters=X['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""

            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Labels','Cluster'],axis=1)
                cluster_label= cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=355)
                x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=1 / 2, random_state=355)

                unseen_test_data = pd.DataFrame(x_test)
                #unseen_test_data_labels = pd.DataFrame(10**y_test)

                #unseen_data = pd.concat([unseen_test_data,unseen_test_data_labels],axis=1)
                print()
                print("Predictions Batch Files")

                unseen_test_data.to_csv("./Prediction_Batch_files/HealthPrem_26092020_131534.csv",header=True,mode='w+',index=False)

                model_finder=tuner.Model_Finder(self.file_object,self.log_writer) # object initialization

                #min max scaling
                # transofrm data
                scaler = MinMaxScaler(feature_range=(0, 1))
                x_train = scaler.fit_transform(x_train)
                x_val = scaler.fit_transform(x_val)
                #y_train = scaler.fit_transform(y_train)
                #y_test = scaler.fit_transform(y_test)
            
                #converting back to dataframe
                x_train = pd.DataFrame(x_train,columns=cols)
                x_val = pd.DataFrame(x_val,columns=cols)
                #y_train = pd.DataFrame(x_train,columns=['expenses'])
                #y_test = pd.DataFrame(x_test,columns=['expenses'])


                #getting the best model for each of the clusters
                best_model_name,best_model=model_finder.get_best_model(x_train,y_train,x_val,y_val)

                #saving the best model to the directory.
                file_op = file_methods.File_Operation(self.file_object,self.log_writer)
                save_model=file_op.save_model(best_model,best_model_name+str(i))

            # logging the successful Training
            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()

        except Exception:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception
