# -*- coding: utf-8 -*-
import numpy as np
import model_fitting as mf
from sklearn import ensemble

path_outcome = r'C:\Users\Nikki\Documents\Data Science\Kaggle\Animal Shelter\Data\outcome.npy'
path_features = r'C:\Users\Nikki\Documents\Data Science\Kaggle\Animal Shelter\Data\features.npy'
path_test = r'C:\Users\Nikki\Documents\Data Science\Kaggle\Animal Shelter\Data\test.npy'

Y = np.load(path_outcome)
X_train = mf.ConvertFeatureIntoNumpyArray(path_features)
X_test = mf.ConvertFeatureIntoNumpyArray(path_test)

#model = ensemble.RandomForestClassifier(n_estimators = 100, max_depth=None, min_samples_split=1)
model = ensemble.GradientBoostingClassifier(n_estimators = 200)

#logloss = mf.CalculateLogLoss(X_train, Y, model)

prediction1 = mf.PredictTestData(X_test, X_train, Y, model)
prediction2 = mf.PredictTestData(X_test, X_train, Y, ensemble.GradientBoostingClassifier(n_estimators = 150, max_depth = 5))
prediction3 = mf.PredictTestData(X_test, X_train, Y, ensemble.GradientBoostingClassifier(n_estimators = 125, subsample = 0.6, learning_rate = 0.15))

prediction = (prediction1 + prediction2 + prediction3)/3

mf.SavePredictionData(prediction)

#feature_importance = model.fit(X_train, Y).feature_importances_
#feature_importance = 100.0 * (feature_importance / feature_importance.max())