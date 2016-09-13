import re
import numpy as np

def parse_column(data, number_column):
    
    feature = [row[number_column] for row in data]   
    
    #remove header
    feature.pop(0)
    return feature

def repeat_string_feature(data, number_column):

    feature = parse_column(data, number_column)

    feature_unique = list(set(feature))
    
    feature_numbered = []

    for entry in feature:
        for index, specific_feature in enumerate(feature_unique):
            if (entry == specific_feature):
                feature_numbered.append(index)
    
    return feature_numbered
    
def split_string_feature(data, number_column, split_char, flag_breed):

    feature_unique = set()
    feature_numbered = []
    feature_numbered2 = []
    feature_dictionary = {}

    index_feature = 1
    
    for index, row in enumerate(data):
        
        if (index != 0):
            entry = row[number_column]
            
            if flag_breed:
                entry = entry.replace(' Mix', '') 
        
            split_data = entry.split(split_char)
            
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
                    print 'Triple data entry ', entry
            
    return (feature_numbered, feature_numbered2)

def extract_age_feature(data, number_column):
    
    feature = parse_column(data, number_column)
    
    feature_numbered = []
    
    for entry in feature:
        
        result = re.match('\d+', entry)
        
        if result:
            number = int(result.group(0))
            
            if re.match('.+years?', entry):
                number = number * 365
            elif re.match('.+months?', entry):
                number = number *  30
            elif re.match('.+weeks?', entry):
                number = number * 7
            elif re.match('.+days?', entry):
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
    
def extract_name_exists(data, number_column):
    
    feature = parse_column(data, number_column)
    
    feature_numbered = []

    for entry in feature:
        
        if not entry:
            feature_numbered.append(0)
        else:
            feature_numbered.append(1)

    return feature_numbered
    
def string_is_present(data, number_column, regex):
    
    feature = parse_column(data, number_column)
    
    feature_numbered = []

    for entry in feature:
        result = 0              
        
        if re.match(regex, entry):
            result = 1
        
        feature_numbered.append(result)
    
    return feature_numbered
    
def scale_feature(entry):
    
    average = np.mean(entry)
    stddev = np.std(entry)
    
    score = (entry - average)/stddev
    return score
    
            