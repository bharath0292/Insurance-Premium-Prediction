from datetime import datetime
from os import listdir
import pandas
from application_logging.logger import App_Logger


class dataTransformPredict:

     def __init__(self):
          self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
          self.logger = App_Logger()


     def addQuotesToStringValuesInColumn(self):

          try:
               log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    data = pandas.read_csv(self.goodDataPath + "/" + file)
                    # list of columns with string datatype variables
                    column = ["age","sex","bmi","children","smoker","region"]

                    for col in data.columns:
                         if col in column:  # add quotes in string value
                              data[col] = data[col].apply(lambda x: "'" + str(x) + "'")
                         if col not in column:  # add quotes to '?' values in integer/float columns
                              data[col] = data[col].replace('?', "'?'")
                    # #csv.update("'"+ csv['Wafer'] +"'")
                    # csv.update(csv['Wafer'].astype(str))
                    # csv['Wafer'] = csv['Wafer'].str[6:]
                    data.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                    self.logger.log(log_file, " %s: Quotes added successfully!!" % file)

          except Exception as e:
               log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
               self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
               #log_file.write("Current Date :: %s" %date +"\t" +"Current time:: %s" % current_time + "\t \t" + "Data Transformation failed because:: %s" % e + "\n")
               log_file.close()
               raise e
          log_file.close()
