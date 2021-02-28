from datetime import datetime
from os import listdir
from application_logging.logger import App_Logger
import pandas as pd


class dataTransform:

    def __init__(self):
        self.goodDataPath = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()

    def addQuotesToStringValuesInColumn(self):

        log_file = open("Training_Logs/addQuotesToStringValuesInColumn.txt", 'a+')
        try:
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                data = pd.read_csv(self.goodDataPath + "/" + file)
                # list of columns with string datatype variables
                column = ['sex', 'age', 'sex', 'bmi', 'children', 'smoker', 'region', 'expenses']

                for col in data.columns:
                    if col in column:  # add quotes in string value
                        data[col] = data[col].apply(lambda x: "'" + str(x) + "'")
                    if col not in column:  # add quotes to '?' values in integer/float columns
                        data[col] = data[col].replace('?', "'?'")
                # #csv.update("'"+ csv['HealthPrem'] +"'")
                # csv.update(csv['HealthPrem'].astype(str))
                # csv['HealthPrem'] = csv['HealthPrem'].str[6:]
                data.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: Quotes added successfully!!" % file)
            # log_file.write("Current Date :: %s" %date +"\t" + "Current time:: %s" % current_time + "\t \t" +  + "\n")
        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            # log_file.write("Current Date :: %s" %date +"\t" +"Current time:: %s" % current_time + "\t \t" + "Data
            # Transformation failed because:: %s" % e + "\n")
            log_file.close()
        log_file.close()
