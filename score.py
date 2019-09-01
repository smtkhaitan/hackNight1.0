import json
import numpy as np
import os
import pickle
from sklearn.externals import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from azureml.core.model import Model

def init():
    global model
    # retrieve the path to the model file using the model name
    model_path = Model.get_model_path('mlp_classifier')
    model = joblib.load(model_path)

def run(raw_data):
    data = pd.DataFrame.from_dict(json.loads(raw_data))
    data['genderNormalized'] = data.apply(lambda row: genderNormalizer(row.Gender), axis=1)
    data_new = MultiColumnLabelEncoder().fit_transform(data.drop('Age',axis=1))
    data_new['Age'] = data['Age']
    # make prediction
    y_hat = model.predict(data_new)
    # you can return any data type as long as it is JSON-serializable
    return y_hat

m = {'Male','male','m','M','Make','Cis Male','Man','cis male'}
f = ['Female','female','F','f','Woman','woman']

def genderNormalizer(gender):
    if gender in m:
        return 'm'
    elif(gender in f):
        return 'f'
    else:
        return '-1'
    
class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)