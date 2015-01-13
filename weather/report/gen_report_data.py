import requests
import datetime
from report.constant import WEATHER_API
import copy

def make_get_request():
    url_params = {
              'id': 1277333,
              'AAPIID': 1111111111
              }
    r = requests.get(WEATHER_API, params=url_params)
    try:
        return r.json()
    except ValueError as exp:
        return {} 


def get_report_data():
    """
    Get the weather report to show on UI
    """
    report_data = make_get_request()
    temp_date_map = get_temp_date_map(report_data)
    min_max_temp_of_day = get_min_max_temp_of_day(temp_date_map)    
    temp_in_increasing_order = get_temp_in_increasing_order(report_data.get('list'))
    return {
            'min_max_temp_of_day': min_max_temp_of_day,
            'temp_in_increasing_order': temp_in_increasing_order
            }


def get_datetime_from_timetamp(timestamp):
    '''
    Return datetime object for the timestamp
    '''
    return datetime.datetime.fromtimestamp(
                            int(timestamp))


def get_temp_in_increasing_order(report_data):
    '''
    sorts the temperature datetime map based on
    temperature 
    '''
    sorted_data = sorted(report_data, key=lambda x: x['main']['temp'])
    # creating a tuple with multiple items. A map is messing up
    # the order of sorted temperature.
    return [(x['main']['temp'], get_datetime_from_timetamp(x['dt']))  for x in sorted_data]


def get_min_max_temp_of_day(temp_date_map):
    """
    Returns the min and max temperature of the day
    along with other info with key as date.
    """
    min_max_temp_map = {}
    for date, values in temp_date_map.items():
        min_temp_dict = min(values, key=lambda x: x['temp_min']) 
        max_temp_dict = max(values, key=lambda x: x['temp_max'])
        min_max_temp_map[date] = {
                                  'min_temp': min_temp_dict,
                                  'max_temp': max_temp_dict
                                  }
    return min_max_temp_map


def get_temp_date_map(report_data):
    """
    Returns date vs weather detail map. This map would
    be apt to generate all kinds of reports based on a
    particular date eg: least/highest 
    humidity, temperature of the day etc
    """
    temp_date_map = {}
    temp_dict = {}
    for data in report_data['list']:
        # Using timestamp instead of text format
        # In case api changes the format of dt_txt
        # handling with python datetime might break.
        temp_date_time = get_datetime_from_timetamp(data['dt'])
        temp_date = temp_date_time.date()
        temp_dict['temp_min'] = data['main']['temp_min']
        temp_dict['temp_max'] = data['main']['temp_max']
        temp_dict['temp'] = data['main']['temp']
        temp_dict['date_time'] = temp_date_time
        if not temp_date_map.get(temp_date):
            temp_date_map[temp_date] = [copy.copy(temp_dict)]
        else:
            temp_date_map[temp_date].append(copy.copy(temp_dict))
    return temp_date_map
