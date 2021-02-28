from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

class Model_Finder:


    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.Linear_reg = LinearRegression()
        self.SVR_reg = SVR()
        self.RF_reg = RandomForestRegressor()
        self.XGB_reg = XGBRegressor(objective='reg:squarederror')


    def get_best_params_for_svr(self,train_x,train_y):

        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_svr method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid = {'C': [0.1, 1, 10, 100, 1000],
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf']}

            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.SVR_reg, param_grid=self.param_grid, cv=5,  verbose=3,n_jobs=-1)
            #finding the best parameters
            self.grid.fit(train_x, train_y)

            #extracting the best parameters
            self.C = self.grid.best_params_['C']
            self.gamma = self.grid.best_params_['gamma']
            self.kernel = self.grid.best_params_['kernel']

            #creating a new model with the best parameters
            self.SVR_reg = SVR(C=self.C, gamma=self.gamma, kernel=self.kernel)
            # training the mew model
            self.SVR_reg.fit(train_x, train_y)
            self.logger_object.log(self.file_object,'Support Vector Machine Regressor best params: '+str(self.grid.best_params_)+'. Exited the get_best_params_for_random_forest method of the Model_Finder class')

            return self.SVR_reg

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in get_best_params_for_svr method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Support Vector Parameter tuning  failed. Exited the get_best_params_for_svr method of the Model_Finder class')
            raise Exception()


    def get_best_params_for_random_forest(self,train_x,train_y):

        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_random_forest method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            #self.param_grid = {"n_estimators": [10, 20, 50, 70, 100, 130], "criterion": ['mse', 'mae'],
                               #"max_depth": range(2, 10, 1), "max_features": ['auto', 'sqrt', 'log2'],
                               #"min_samples_split": [2, 5, 10, 14], "min_samples_leaf": [1, 2, 4, 6, 8]}

            
            self.param_grid = {"n_estimators": [10,20], "criterion": ['mse'],
                               "max_depth": range(2, 5, 1), "max_features": ['sqrt'],
                               "min_samples_split": [2, 5], "min_samples_leaf": [1, 2]}

            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.RF_reg, param_grid=self.param_grid, cv=3, verbose=3,n_jobs=-1)
            #finding the best parameters
            self.grid.fit(train_x, train_y)

            #extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.min_samples_split = self.grid.best_params_['min_samples_split']
            self.min_samples_leaf = self.grid.best_params_['min_samples_leaf']

            #creating a new model with the best parameters
            self.RF_reg = RandomForestRegressor(n_estimators=self.n_estimators, criterion=self.criterion,
                                                max_depth=self.max_depth, max_features=self.max_features,
                                                min_samples_split=self.min_samples_split,
                                                min_samples_leaf=self.min_samples_leaf)
            # training the mew model
            self.RF_reg.fit(train_x, train_y)
            self.logger_object.log(self.file_object,'Random Forest best params: '+str(self.grid.best_params_)+'. Exited the get_best_params_for_random_forest method of the Model_Finder class')

            return self.RF_reg

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in get_best_params_for_random_forest method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Random Forest Parameter tuning  failed. Exited the get_best_params_for_random_forest method of the Model_Finder class')
            raise Exception()

    def get_best_params_for_xgboost(self,train_x,train_y):

        self.logger_object.log(self.file_object,'Entered the get_best_params_for_xgboost method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid_xgboost = {

                'learning_rate': [0.5, 0.1, 0.01, 0.03, 0.08, 0.001],
                'max_depth': [3, 5, 10, 20, 50],
                'n_estimators': [10, 50, 100, 200, 300]

            }
            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(XGBRegressor(objective='reg:squarederror'),self.param_grid_xgboost, verbose=3, cv=5,n_jobs=-1)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.XGB_reg = XGBRegressor(learning_rate=1, max_depth=5, n_estimators=50)
            # training the mew model
            self.XGB_reg.fit(train_x, train_y)
            self.logger_object.log(self.file_object,
                                   'XGBoost best params: ' + str(self.grid.best_params_) + '. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            return self.XGB_reg

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_xgboost method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'XGBoost Parameter tuning  failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise Exception()


    def get_best_model(self,train_x,train_y,test_x,test_y):

        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')

        try:
            # create best model for Linear Regression
            self.Linear_reg.fit(train_x, train_y)
            self.prediction_Linear_reg = self.Linear_reg.predict(test_x)  # Predictions using the Linear Regression Model

            self.Linear_reg_score = mean_squared_error(test_y, self.prediction_Linear_reg)
            self.logger_object.log(self.file_object, 'MSE for Linear Regression:' + str(self.Linear_reg_score))


            # create best model for Support Vector Regression
            #self.SVR=self.get_best_params_for_svr(train_x,train_y)
            #self.prediction_SVR= self.SVR.predict(test_x)  # Predictions using the Support Vector Regression Model

            #self.SVR_score = mean_squared_error(test_y, self.prediction_SVR)
            #self.logger_object.log(self.file_object, 'MSE for Support Vector Regression:' + str(self.SVR_score))


            # create best model for Random Forest
            self.Random_Forest_reg=self.get_best_params_for_random_forest(train_x,train_y) # @todo need to check taking too long
            self.prediction_Random_Forest_reg=self.Random_Forest_reg.predict(test_x) # prediction using the Random Forest Algorithm

            self.Random_Forest_reg_score = mean_squared_error(test_y,self.prediction_Random_Forest_reg)
            self.logger_object.log(self.file_object, 'MSE for Random Forest Regression:' + str(self.Random_Forest_reg_score))


            # create best model for XGBoost
            self.Xgboost_reg = self.get_best_params_for_xgboost(train_x, train_y)
            self.prediction_Xgboost_reg = self.Xgboost_reg.predict(test_x)  # Predictions using the XGBoost Model
            
            self.logger_object.log(self.file_object, 'Value for prediction_Xgboost_reg predicted:' + str(self.prediction_Xgboost_reg))
            

            self.Xgboost_reg_score = mean_squared_error(test_y, self.prediction_Xgboost_reg)
            self.logger_object.log(self.file_object, 'Value for test_y predicted:' + str(test_y))
            self.logger_object.log(self.file_object, 'MSE for XGBoost Regression:' + str(self.Xgboost_reg_score))


            #comparing all the models
            score_list = [self.Linear_reg_score,self.Random_Forest_reg_score,self.Xgboost_reg_score]
            self.logger_object.log(self.file_object, 'Value for score_list' + str(score_list))
            if (self.Linear_reg_score==max(score_list)):
                return 'LinearRegression',self.Linear_reg
           # elif (self.SVR_score==max(score_list)):
                #return 'SupportVector',self.SVR
            elif (self.Random_Forest_reg_score==max(score_list)):
                return 'RandomForest',self.Random_Forest_reg
            elif (self.Xgboost_reg_score==max(score_list)):
                return 'XGBoost',self.Xgboost_reg

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()