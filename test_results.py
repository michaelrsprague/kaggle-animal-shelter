# -*- coding: utf-8 -*-
import os.path
import numpy as np
import model_fitting as mf
from sklearn import ensemble

root_path = r'C:\GitRepository\kaggle-animal-shelter\Data'

path_outcome = os.path.join(root_path, 'outcome.npy')
path_features = os.path.join(root_path, 'features.npy')
path_test = os.path.join(root_path, 'test.npy')

Y = np.load(path_outcome)
X_train = mf.ConvertFeatureIntoNumpyArray(path_features)
X_test = mf.ConvertFeatureIntoNumpyArray(path_test)

model = ensemble.GradientBoostingClassifier(n_estimators = 100)

#perform k-fold cross-validation
logloss = mf.CalculateLogLoss(X_train, Y, model)

#prediction = mf.PredictTestData(X_test, X_train, Y, model)
#mf.SavePredictionData(prediction)

#examine relative importance of features
#feature_importance = model.fit(X_train, Y).feature_importances_
#feature_importance = 100.0 * (feature_importance / feature_importance.max())