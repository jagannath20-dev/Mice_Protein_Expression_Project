from mice.exception import MiceException
from mice.logger import logging
from mice.config import mongo_client
import os , sys
from mice.utils import get_collection_as_dataframe
from mice.entity import config_entity,artifact_entity
from mice.components.data_ingestion import DataIngestion




print(__name__)
if __name__ == "__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          #data ingestion
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
          

     except Exception as e:
          print(e)