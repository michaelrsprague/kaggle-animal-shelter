import numpy as np
import os.path
import extract_features

data_folder = r'C:\GitRepository\kaggle-animal-shelter\Data'

path_train = os.path.join(data_folder, 'train.csv')
path_test = os.path.join(data_folder, 'test.csv')

#outcome is the reported classification
outcome = extract_features.extract_outcomes(path_train)
data = extract_features.extract_features(path_train)
test = extract_features.extract_features(path_test)

data_array = np.array(data)
outcome_array = np.array(outcome)
test_array = np.array(test)

#save data to file for future analysis
features_path = os.path.join(data_folder, 'features')
np.save(features_path, data_array)

outcome_path = os.path.join(data_folder, 'outcome')
np.save(outcome_path, outcome_array)

test_path = os.path.join(data_folder, 'test')
np.save(test_path, test_array)