import sys,os
import pandas as pd 
from mice.exception import MiceException
from mice.logger import logging
from datetime import datetime

FILE_NAME = "mice.csv"
TRAIN_FILE_NAME = "mice_train.csv"
TEST_FILE_NAME = "mice_test.csv"


class TrainingPipelineConfig:


     def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception  as e:
            raise MiceException(e,sys)


class DataIngestionConfig:

    def __init__(self,training_pipeline_config: TrainingPipelineConfig):

        try:
            self.database_name = "mice_preotein"
            self.collection_name = "Mice"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_Store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2


        except Exception as e:
            raise MiceException(e,sys)

    
    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise MiceException(e,sys)




class DataValidationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
        self.missing_threshold = 0.2
        self.base_file_path = os.path.join("mice.csv")




class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluatorConfig:...
class ModelPusherConfig:...