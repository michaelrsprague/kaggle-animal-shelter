import datetime
import numpy as np

def extract_date_time(data_input, number_column):
    
    feature = [row[number_column] for row in data_input]
    
    #remove header
    feature.pop(0)
    
    format_datetime = "%Y-%m-%d  %H:%M:%S"
    feature_numbered = [datetime.datetime.strptime(data, format_datetime)
                        for data in feature]    
        
    return feature_numbered
    
def extract_year(date_time):
    
    return [dt.year for dt in date_time]
    
def extract_month(date_time):
    
    return [dt.month for dt in date_time]
    
def extract_day(date_time):
    
    return [dt.day for dt in date_time]
    
def extract_hour(date_time):
    
    return [dt.hour for dt in date_time]

def extract_minute(date_time):  
   
    return [dt.minute for dt in date_time]

def extract_dayweek(date_time):
    
    return [dt.weekday() for dt in date_time]
    
def extract_sametime(date_time):
    
    sametime = np.zeros(len(date_time))
    minute_range = 3
     
    sort_index = np.array(date_time).argsort() 
    
    for index, sort in enumerate(sort_index):
        
        if (index == 0):            
            time_difference_fw = date_time[sort_index[index + 1]] - date_time[sort_index[index]]
            result = abs(time_difference_fw) < datetime.timedelta(0, 60 * minute_range)
            
        elif (index == len(sort_index) - 1):            
            time_difference_rv = date_time[sort_index[index]] - date_time[sort_index[index - 1]]
            result = abs(time_difference_rv) < datetime.timedelta(0, 60 * minute_range)
              
        else:            
            time_difference_fw = date_time[sort_index[index + 1]] - date_time[sort_index[index]]
            time_difference_rv = date_time[sort_index[index]] - date_time[sort_index[index - 1]]
            result = (abs(time_difference_rv) < datetime.timedelta(0, 60 * minute_range)) or (abs(time_difference_fw) < datetime.timedelta(0, 60 * minute_range))
                  
        sametime[sort_index[index]] = result                                                      
    
    return list(sametime)        
    
def extract_partday(date_time):
    
    partday = []
    
    for dt in date_time:
        
        result = 0;
        
        if (dt.hour >= 8 and dt.hour < 11):
            result = 0
        elif (dt.hour >= 11 and dt.hour < 15):
            result = 1
        elif (dt.hour >= 15 and dt.hour < 19):
            result = 2
        else:
            result = 3
        
        partday.append(result)
                    
    return partday
    
def extract_holidays(date_time):
    
    is_holidays = []
    holidays = [datetime.date(2013, 1, 1),
                datetime.date(2013, 1, 21),
                datetime.date(2013, 2, 18),
                datetime.date(2013, 3, 29),
                datetime.date(2013, 5, 27),
                datetime.date(2013, 7, 4),
                datetime.date(2013, 9, 2),
                datetime.date(2013, 11, 28),
                datetime.date(2013, 12, 25),
                datetime.date(2013, 12, 26),
                datetime.date(2014, 1, 1),
                datetime.date(2014, 1, 20),
                datetime.date(2014, 2, 17),
                datetime.date(2014, 4, 18),
                datetime.date(2014, 5, 26),
                datetime.date(2014, 7, 4), 
                datetime.date(2014, 9, 1),
                datetime.date(2014, 11, 27),
                datetime.date(2014, 12, 25),
                datetime.date(2014, 12, 26),
                datetime.date(2015, 1, 1),
                datetime.date(2015, 1, 19),
                datetime.date(2015, 2, 16),
                datetime.date(2015, 4, 3),
                datetime.date(2015, 5, 25),
                datetime.date(2015, 7, 3), 
                datetime.date(2015, 9, 7),
                datetime.date(2015, 11, 26),
                datetime.date(2015, 12, 25),
                datetime.date(2015, 12, 28),
                datetime.date(2016, 1, 1),
                datetime.date(2016, 1, 18),
                datetime.date(2016, 2, 15)]
    
    for dt in date_time:
        
        result = 0;
        
        date = dt.date()        
                                
        if date in holidays:
            result = 1
        
        is_holidays.append(result)
                    
    return is_holidays