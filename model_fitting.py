from sklearn import metrics, ensemble, cross_validation
import numpy as np
import csv

def PredictLogLoss(model, X_train, X_test, Y_train, Y_test):    
    
    model.fit(X_train, Y_train)
    prediction = model.predict_proba(X_test)
    logloss = metrics.log_loss(Y_test, prediction)
     
    return logloss
    
def ConvertFeatureIntoNumpyArray(path_features):
    features = np.load(path_features)
    
    number_features = np.size(features, 0)
    number_samples = np.size(features, 1)
    
    X = np.empty([number_samples, number_features])

    for index, feature in enumerate(features):
        X[:,index] = np.array(feature)
    
    return X
    
def CalculateLogLoss(X, Y, model):
    cv = cross_validation.KFold(len(Y), n_folds = 6, shuffle = True) 

    logloss = []

    for train_index, test_index in cv:
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
    
        logloss.append(PredictLogLoss(model, X_train, X_test, Y_train, Y_test))
    
    mean_logloss = np.mean(logloss)
    print 'Mean logloss for Model = ', mean_logloss
    
    return mean_logloss

def PredictTestData(X_test, X_train, Y_train, model):
        
    model.fit(X_train, Y_train)
    
    return model.predict_proba(X_test)
    
def SavePredictionData(prediction):
        
    with open(r'C:\Users\Nikki\Documents\Data Science\Kaggle\Animal Shelter\Data\prediction.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        csvwriter.writerow(['ID','Adoption','Died', 'Euthanasia', 'Return_to_owner','Transfer'])
        
        for row in range(0, np.size(prediction, 0)):
            csvwriter.writerow((row + 1, prediction[row, 1], prediction[row, 3], prediction[row, 4], prediction[row, 2], prediction[row, 0]))   
