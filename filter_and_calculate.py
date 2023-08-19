import math

EARTH_RADIUS = 3958.8


def distance(lat1: float, long1: float, lat2: float, long2: float) -> float:
    """
    Calculate the distance from one coordinate to another.
    
    Return: Distance in miles.
    """
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    long1 = math.radians(long1)
    long2 = math.radians(long2)
    if lat2 > lat1:
        dlat = lat2 - lat1
    else:
        dlat = lat1 - lat2
    if long2 > long1:
        dlong = long2 - long1
    else:
        dlong = long1 - long2
    alat = (lat1 + lat2) / 2
    math.radians(alat)
    x = dlong * math.cos(alat)
    return math.sqrt(x ** 2 + dlat ** 2) * EARTH_RADIUS


def p_to_aqi(data: list) -> list:
    """Convert all pm in data list to AQI."""
    concentration = {(0.0, 12.0): (0, 50), (12.1, 35.4): (51, 100), (35.5, 55.4): 
    (101, 150), (55.5, 150.4): (151, 200), 
    (150.5, 250.4): (201, 300), (250.5, 350.4):
    (301, 400), (350.5, 500.4): (401, 500)}
    for i in data:
        flag = False
        for limits in concentration:
            if (i[1] != None):
                if (limits[0] <= i[1] <= limits[1]):
                    flag = True
                    ratio = (i[1] - limits[0]) / (limits[1] - limits[0])
                    aqi = (concentration[limits][1] - concentration[limits][0]) * ratio + concentration[limits][0]
                    i[1] = round(aqi)
        if not flag:
            i[1] = 501
    return data
        

def threshold_filter(data: list, threshold_value: int) -> list:
    """Filter out the data from sensors with AQI below the threshhold."""
    final_data = []
    for i in data:
        if (i[1] >= threshold_value) or (i[1] != None):
            final_data.append(i)
    return final_data


def outdoor_filter(data: list) -> list:
    """Filter out the data from sensors that are placed indoors."""
    final_data = []
    for i in data:
        if (int(i[25]) == 0) or (i[25] != None):
            final_data.append(i)
    return final_data
    

def age_filter(data: list) -> list:
    """Filter out the data from sensors if readings were taken more than an hour ago."""
    final_data = []
    for i in data:
        if (int(i[4]) <= 3600) or (i[4] != None):
            final_data.append(i)
    return final_data


def range_distance(data: list, range: int, center_lat: float, center_lon: float) -> list:
    """Filter out the data of the sensor farther than the specified range."""
    final_data = []
    for i in data:
        if (i[27] == None) or (i[28] == None):
            data.remove(i)
            continue
        dist = distance(float(center_lat), float(center_lon), float(i[27]), float(i[28]))
        if dist <= range:
            final_data.append(i)
    return final_data


def descending_and_max(data: list, max_data: int) -> list:
    """Arrange data in descending order according to AQI and take the first few entries."""
    d = {}
    for i in data:
        d[i[1]] = i
    d = dict(reversed(sorted(list(d.items()))))
    lst = [x for x in d.values()]
    lst = lst[0:max_data]
    return lst
