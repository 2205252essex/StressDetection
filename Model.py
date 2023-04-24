# -*- coding: utf-8 -*-
"""Copy of Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FcoxEuEgipCjrANo_sWnDXQGe33n-iry

Importing the dataset
"""

from google.colab import drive
import os
import pandas as pd

def import_dataset():
	
  drive.mount('/content/gdrive', force_remount=True)
  input=os.path.join('./CE888/Data/','combined_lagEDA.csv')
  input=os.path.join(os.path.join('gdrive', 'MyDrive', input))
  df=pd.read_csv(input)
  return df

"""Function to calculate performance"""

from sklearn.metrics import classification_report, f1_score, accuracy_score
import numpy as np

def calculate_performance(y_true, y_pred):
     

  acc = accuracy_score(y_true, y_pred)
  print('Accuracy Score: ', acc)

  f1score=f1_score(y_true, y_pred, average='macro')
  print('F1 Score(macro): ', f1score)


  print(classification_report(y_true, y_pred))

"""Print Accuracy"""

def print_accuracy(scores):
  print('Fold accuracy', scores['test_accuracy'])
  print('Average accuracy', np.mean(scores['test_accuracy']))

"""Data Preprocessing"""

def preprocess_data(df_input):
  processed_dataframe=df_input.drop(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'],axis=1)
  input_array = processed_dataframe.drop(['Stress'], axis=1).to_numpy()
  output_array = processed_dataframe.loc[:,'Stress'].to_numpy()
  print(input_array.shape)
  print(output_array.shape)
  return input_array,output_array

"""Importing the libraries"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import RidgeClassifier
from sklearn.tree import DecisionTreeClassifier

"""Calling the functions for import"""

df_input=import_dataset()
input_array,output_array=preprocess_data(df_input)

"""Data Splitting"""

input_train, input_test, output_train, output_test = train_test_split(input_array, output_array, test_size=0.2, stratify=output_array)

"""Grid Search CV based SVM model"""

cv_svc = StratifiedKFold(shuffle=True,n_splits=10)
svm=SVC()

pipe_svc = Pipeline([('scaler',MinMaxScaler()),('svm',svm)])  # build pipeline
param_grid_svc = {
                 'svm__kernel':['linear', 'poly'],
                 'svm__gamma':['scale', 'auto'],
                
                 }
search_svc = GridSearchCV(pipe_svc, param_grid_svc, n_jobs=-1)
scores_svc = cross_validate(search_svc, input_train, output_train, scoring=['accuracy'], cv=cv_svc, return_estimator=True)

"""Calculating Accuracy"""

print_accuracy(scores_svc)

y_predict = cross_val_predict(pipe_svc, input_train, output_train, cv=cv_svc)

calculate_performance(output_train,y_predict)

#Model evaluation on Test Data
search_svc.fit(input_train,output_train)
test_pred=search_svc.best_estimator_.predict(input_test)

calculate_performance(output_test,test_pred)

"""Grid Search cv based DT model"""

cv_DT = StratifiedKFold(shuffle=True,n_splits=10)
dt=DecisionTreeClassifier()

pipe_DT = Pipeline([('scaler',MinMaxScaler()),('dt', dt)])  # build pipeline
param_grid_DT = {
                 'dt__random_state':[0, 1, 2, 3, 4, 5, 10, 15,20,35,50],
                 'dt__criterion':['gini','entropy'],
                 }
search_DT = GridSearchCV(pipe_DT, param_grid_DT, n_jobs=-1)
scores_DT = cross_validate(search_DT, input_train, output_train, scoring=['accuracy'], cv=cv_DT, return_estimator=True)

"""Calculating Accuracy"""

print_accuracy(scores_DT)

y_predict = cross_val_predict(pipe_DT, input_train, output_train, cv=cv_DT)

calculate_performance(output_train,y_predict)

#Model evaluation on Test Data
search_DT.fit(input_train,output_train)
test_pred=search_DT.best_estimator_.predict(input_test)

calculate_performance(output_test,test_pred)