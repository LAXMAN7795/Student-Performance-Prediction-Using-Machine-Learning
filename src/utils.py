import os
import sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj) #helps to create the pickle files

    except Exception as e:
        raise CustomException(e,sys)

def evaluate_model(X_train, y_train, X_test, y_test, models,param):
    """
    Evaluate multiple models and return their scores.
    """
    try:
        models_report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para= param[list(models.keys())[i]]

            gs = GridSearchCV(
                estimator=model,
                param_grid=para,
                cv=3,
            )

            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_score = r2_score(y_train, y_train_pred)
            test_score = r2_score(y_test, y_test_pred)

            models_report[list(models.keys())[i]] = {
                "train_score": train_score,
                "test_score": test_score
            }

        return models_report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    """
    Load an object from a file.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)