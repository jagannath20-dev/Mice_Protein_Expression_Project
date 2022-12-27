from mice.logger import logging
from mice.exception import MiceException
from mice import utils
from mice.entity import config_entity
from mice.entity import artifact_entity
import os, sys
import numpy as np
import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from mice.config import TARGET_COLUMN
from typing import Optional


class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise MoceException(e,sys)


    @classmethod
    
    def get_data_transformer_object(cls) -> Pipeline:

        try:
            simple_imputer = SimpleImputer(strategy='constant',fill_value = 0)
            standar_scaler = StandardScaler()
            pipeline = Pipeline(steps=[
                ('Imputer',simple_imputer),
                ('StandardScaler',standar_scaler)
            ])
            return pipeline
        except Exception as e:
            raise MiceException(e,sys)

    def initiate_data_transformation(self)-> artifact_entity.DataTransformationArtifact:

        try:
            # Reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            train_df['Genotype']=train_df['Genotype'].map({'Control':0, 'Ts65Dn':1})
            train_df['Treatment']=train_df['Treatment'].map({'Saline':0, 'Memantine':1})
            train_df['Behavior']=train_df['Behavior'].map({'C/S':0, 'S/C':1 })

            test_df['Genotype']=test_df['Genotype'].map({'Control':0, 'Ts65Dn':1})
            test_df['Treatment']=test_df['Treatment'].map({'Saline':0, 'Memantine':1})
            test_df['Behavior']=test_df['Behavior'].map({'C/S':0, 'S/C':1 })

            label_encoder = LabelEncoder()


            train_df['class'] =label_encoder.fit_transform(train_df['class'])
            test_df['class'] =label_encoder.fit_transform(test_df['class']) 

            # Selecting input features for train and test dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis = 1)
            input_feature_test_df  = test_df.drop(TARGET_COLUMN,axis =1)

            # Selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]
            

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)
            label_encoder.fit(target_feature_test_df)

           # transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)
            transformation_pipeline.fit(input_feature_test_df)

            # transformation on input features
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr  = transformation_pipeline.transform(input_feature_test_df)

            smt = SMOTETomek()
            logging.info(f"Before resampling in training set Input: {input_feature_train_arr.shape} Target: {target_feature_train_arr.shape}")
            input_feature_train_arr,target_feature_train_arr = smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"After resampling in training set input: {input_feature_train_arr.shape} Target: {target_feature_train_arr.shape}")

            logging.info(f"Before resampling in the testing set Input : {input_feature_test_arr.shape} Target: {target_feature_test_arr.shape}")
            input_featue_test_arr,target_feature_test_arr = smt.fit_resample(input_feature_test_arr,target_feature_test_arr)
            logging.info(f"After resampling in the testing set Input: {input_feature_test_arr.shape} Target: {target_feature_test_arr.shape}")
            

            # Target Encoder

            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr  = np.c_[input_featue_test_arr,target_feature_test_arr]

            #Save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array =train_arr)
            
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array = test_arr)

                    
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
                                        obj = transformation_pipeline)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
                                        obj = label_encoder)

            
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transfromed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path= self.data_transformation_config.target_encoder_path
            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact


        except Exception as e:
            raise MiceException(e,sys)

