import re
import numpy as np

def parse_column(reader, number_column):
    feature = []

    for row in reader:
        feature.append(row[number_column])
    
    #remove header
    feature.pop(0)
    return feature

def repeat_string_feature(reader, number_column):

    feature = parse_column(reader, number_column)

    feature_unique = list(set(feature))
    
    feature_numbered = []

    for data in feature:
        for index, specific_feature in enumerate(feature_unique):
            if (data == specific_feature):
                feature_numbered.append(index)
    
    return feature_numbered
    
def split_string_feature(reader, number_column, split_char, flag_breed):

    feature_unique = set()
    feature_numbered = []
    feature_numbered2 = []
    feature_dictionary = {}

    index_feature = 1
    
    for index, row in enumerate(reader):
        
        if (index != 0):
            data = row[number_column]
            
            if flag_breed:
                data = data.replace(' Mix', '') 
        
            split_data = data.split(split_char)
            
            count = 0
            
            for element in split_data:
                
                if element not in feature_unique:             
                    feature_unique.add(element)
                    feature_dictionary[element] = index_feature
                    index_feature += 1                 

                if count == 0:
                    feature_numbered.append(feature_dictionary[element])
                    feature_numbered2.append(0)
                    count += 1
                elif count == 1:
                    feature_numbered2[-1] = feature_dictionary[element]
                    count += 1
                else:
                    print 'Triple data entry ', data
            
    return (feature_numbered, feature_numbered2)

def extract_age_feature(reader, number_column):
    
    feature = parse_column(reader, number_column)
    
    feature_numbered = []
    
    for data in feature:
        
        result = re.match('\d+', data)
        
        if result:
            number = int(result.group(0))
            
            if re.match('.+years?', data):
                number = number * 365
            elif re.match('.+months?', data):
                number = number *  30
            elif re.match('.+weeks?', data):
                number = number * 7
            elif re.match('.+days?', data):
                number = number
            else:
                raise ValueError("The data includes an age type that was not expected")     
        
            feature_numbered.append(number)      
            number = 0
            
        else:
            number = 365
            feature_numbered.append(number)        
            number = 0 
          
    return feature_numbered

def classify_age_groups(age_days):
    
    age_group = []
    
    for age in age_days:
        
        group = 0
        
        if age <= 180:
            group = 0
        elif age > 180 and age <= 365*2:
            group = 1
        elif age > 365*2 and age <= 365*10:
            group = 2
        else:
            group = 3
    
        age_group.append(group)
    
    return age_group
    
def extract_name_exists(reader, number_column):
    
    feature = parse_column(reader, number_column)
    
    feature_numbered = []

    for data in feature:
        
        if not data:
            feature_numbered.append(0)
        else:
            feature_numbered.append(1)

    return feature_numbered
    
def string_is_present(reader, number_column, regex):
    
    feature = parse_column(reader, number_column)
    
    feature_numbered = []

    for data in feature:
        result = 0              
        
        if re.match(regex, data):
            result = 1
        
        feature_numbered.append(result)
    
    return feature_numbered
    
def scale_feature(data):
    
    average = np.mean(data)
    stddev = np.std(data)
    
    score = (data - average)/stddev
    return score
    
            