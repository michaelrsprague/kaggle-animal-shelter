import csv
import numpy as np
import os.path
import features
import features_datetime

def extract_datetime_features(data, date_time):
        
    event_year = features_datetime.extract_year(date_time)
    data.append(event_year)

    event_month = features_datetime.extract_month(date_time)
    data.append(event_month)

    event_day = features_datetime.extract_day(date_time)
    data.append(event_day)

    event_hour = features_datetime.extract_hour(date_time)
    data.append(event_hour)

    event_minute = features_datetime.extract_minute(date_time)
    data.append(event_minute)

    event_day_of_year = [(month - 1)*30 + day for month,day in zip(event_month, event_day)]
    data.append(event_day_of_year)

    event_start_dataset = [(year - 2013)*12 + (month - 10) for year, month in zip(event_year, event_month)]
    data.append(event_start_dataset)

    event_dayweek = features_datetime.extract_dayweek(date_time)
    data.append(event_dayweek)
    
    event_sametime = features_datetime.extract_sametime(date_time)
    data.append(event_sametime)
    
    event_partday = features_datetime.extract_partday(date_time)
    data.append(event_partday)
    
    event_holiday = features_datetime.extract_holidays(date_time)
    data.append(event_holiday)
    
    return data

def ExtractFeatures(file_path):
    
    file_id = open(file_path)
    reader = csv.reader(file_id)
    
    data = []
    
    #animal type
    animal_type = features.repeat_string_feature(reader, 5)
    data.append(animal_type)
    file_id.seek(0)

    #sex
    animal_sex = features.string_is_present(reader, 6, '.+[mM]ale')
    data.append(animal_sex)
    file_id.seek(0)
    
    #intact
    animal_intact = features.string_is_present(reader, 6, 'Intact')
    data.append(animal_intact)
    file_id.seek(0)

    #breed
    animal_breed, second_animal_breed = features.split_string_feature(reader, 8, '/', True)
    data.append(animal_breed)
    data.append(second_animal_breed)
    file_id.seek(0)

    #colour
    animal_colour, second_animal_colour = features.split_string_feature(reader, 9, '/', False)
    file_id.seek(0)
    data.append(animal_colour)
    data.append(second_animal_colour)

    #age in days
    age_days = features.extract_age_feature(reader, 7)
    age_group = features.classify_age_groups(age_days)
    age_days_log = np.log10(age_days)
    age_days_log[age_days_log == -np.inf] = 0;
    
    data.append(age_days)
    data.append(age_days_log)
    data.append(age_group)
    file_id.seek(0)

    #name exists?
    name_exists = features.extract_name_exists(reader, 1)
    data.append(name_exists)
    file_id.seek(0)

    #date/time outcome
    date_time = features_datetime.extract_date_time(reader, 2)
    data = extract_datetime_features(data, date_time)

    file_id.close()
    return data

def ExtractTestFeatures(file_path):
    
    file_id = open(file_path)
    reader = csv.reader(file_id)
    
    data = []
    
    #animal type
    animal_type = features.repeat_string_feature(reader, 3)
    data.append(animal_type)
    file_id.seek(0)

    #sex
    animal_sex = features.string_is_present(reader, 4, '.+[mM]ale')
    data.append(animal_sex)
    file_id.seek(0)
    
    #intact
    animal_intact = features.string_is_present(reader, 4, 'Intact')
    data.append(animal_intact)
    file_id.seek(0)

    #breed
    animal_breed, second_animal_breed = features.split_string_feature(reader, 6, '/', True)
    data.append(animal_breed)
    data.append(second_animal_breed)
    file_id.seek(0)

    #colour
    animal_colour, second_animal_colour = features.split_string_feature(reader, 7, '/', False)
    file_id.seek(0)
    data.append(animal_colour)
    data.append(second_animal_colour)

    #age in days
    age_days = features.extract_age_feature(reader, 5)        
    age_group = features.classify_age_groups(age_days)
    
    age_days_log = np.log10(age_days)
    age_days_log[age_days_log == -np.inf] = 0;
    
    data.append(age_days)
    data.append(age_days_log)
    data.append(age_group)
    file_id.seek(0)

    #name exists?
    name_exists = features.extract_name_exists(reader, 1)
    data.append(name_exists)
    file_id.seek(0)
    
    #date/time outcome
    date_time = features_datetime.extract_date_time(reader, 2)
    data = extract_datetime_features(data, date_time)

    file_id.close()
    return data

def ExtractOutcomes(file_path):
    file_id = open(file_path)
    reader = csv.reader(file_id)

    outcome = features.repeat_string_feature(reader, 3)
    file_id.close()
    
    return outcome

data_folder = r'C:\GitRepository\kaggle-animal-shelter\Data'

path_train = os.path.join(data_folder, 'train.csv')
path_test = os.path.join(data_folder, 'test.csv')

#outcome is the reported classification
outcome = ExtractOutcomes(path_train)
data = ExtractFeatures(path_train)

test = ExtractTestFeatures(path_test)

data_array = np.array(data)
outcome_array = np.array(outcome)
test_array = np.array(test)

features_path = os.path.join(data_folder, 'features')
np.save(features_path, data_array)

outcome_path = os.path.join(data_folder, 'outcome')
np.save(outcome_path, outcome_array)

test_path = os.path.join(data_folder, 'test')
np.save(test_path, test_array)