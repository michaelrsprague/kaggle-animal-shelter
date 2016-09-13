import csv
import numpy as np
import features
import features_datetime

def extract_datetime_features(data_features, date_time):
        
    event_year = features_datetime.extract_year(date_time)
    data_features.append(event_year)

    event_month = features_datetime.extract_month(date_time)
    data_features.append(event_month)

    event_day = features_datetime.extract_day(date_time)
    data_features.append(event_day)

    event_hour = features_datetime.extract_hour(date_time)
    data_features.append(event_hour)

    event_minute = features_datetime.extract_minute(date_time)
    data_features.append(event_minute)

    event_day_of_year = [(month - 1)*30 + day for month,day in zip(event_month, event_day)]
    data_features.append(event_day_of_year)

    event_start_dataset = [(year - 2013)*12 + (month - 10) for year, month in zip(event_year, event_month)]
    data_features.append(event_start_dataset)

    event_dayweek = features_datetime.extract_dayweek(date_time)
    data_features.append(event_dayweek)
    
    event_sametime = features_datetime.extract_sametime(date_time)
    data_features.append(event_sametime)
    
    event_partday = features_datetime.extract_partday(date_time)
    data_features.append(event_partday)
    
    event_holiday = features_datetime.extract_holidays(date_time)
    data_features.append(event_holiday)
    
    return data_features

def extract_features(file_path):
    
    file_id = open(file_path)
    reader = csv.reader(file_id)
    
    data = list(reader)       
    file_id.close()
    
    data_features = []
    
    #strip out category label of data
    header = data[0]
    
    #animal type
    animal_type = features.repeat_string_feature(data, header.index('AnimalType'))
    data_features.append(animal_type)

    #sex
    animal_sex = features.string_is_present(data, header.index('SexuponOutcome'), '.+[mM]ale')
    data_features.append(animal_sex)
    
    #intact
    animal_intact = features.string_is_present(data, header.index('SexuponOutcome'), 'Intact')
    data_features.append(animal_intact)

    #breed
    animal_breed, second_animal_breed = features.split_string_feature(data, header.index('Breed'), '/', True)
    data_features.append(animal_breed)
    data_features.append(second_animal_breed)

    #colour
    animal_colour, second_animal_colour = features.split_string_feature(data, header.index('Color'), '/', False)
    data_features.append(animal_colour)
    data_features.append(second_animal_colour)    
     
    #age in days
    age_days = features.extract_age_feature(data, header.index('AgeuponOutcome'))
    age_group = features.classify_age_groups(age_days)
    age_days_log = np.log10(age_days)
    age_days_log[age_days_log == -np.inf] = 0;
    
    data_features.append(age_days)
    data_features.append(age_days_log)
    data_features.append(age_group)

    #name exists?
    name_exists = features.extract_name_exists(data, header.index('Name'))
    data_features.append(name_exists)

    #date/time outcome
    date_time = features_datetime.extract_date_time(data, header.index('DateTime'))
    data_features = extract_datetime_features(data_features, date_time)

    return data_features

def extract_outcomes(file_path):
    
    file_id = open(file_path)
    reader = csv.reader(file_id)

    outcome = features.repeat_string_feature(list(reader), 3)
    file_id.close()
    
    return outcome