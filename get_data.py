import json
import urllib.request
import urllib.parse
import urllib.error
import sys

PURPLEAIR_URL = 'https://www.purpleair.com/data.json'


def file_data(file_path: str) -> dict:
    """Read the file for which the path is specified and return data."""
    try:
        with open(file_path, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print('FAILED')
        print(file_path)
        print('MISSING')
    except TypeError:
        print('FAILED')
        print(file_path)
        print('FORMAT')
    finally:
        f.close()


def api_data(url: str, file_name: str, referer = False) -> dict:
    """Download data from the given URL."""
    try:
        request = urllib.request.Request(url)
        if referer:
            request.add_header('Referer', "Add your header to access api")
        response = urllib.request.urlopen(request)
    except:
        print('FAILED')
        print(url)
        print('NETWORK')
    try:
        encoded_text = response.read().decode(encoding = 'utf-8')
    except urllib.error.HTTPError as e:
        print('FAILED')
        print(e.code,' ', url)
        print('NOT 200')
    except:
        print('FAILED')
        print(url)
        print('NETWORK')
        sys.exit(0)
    finally:
        response.close()
    try:
        data = json.loads(encoded_text)
    except:
        print('FAILED')
        print(url)
        print('FORMAT')
        sys.exit(0)
    write_to_file(data, file_name)
    return data
    
    
def write_to_file(data: dict, file_name: str) -> None:
    """Store the given data in a new file."""
    with open(file_name, 'w') as f:
        json.dump(data, f)
        

def forward_geo_url(center_location: str) -> str:
    """Create URL for forward geocoding using the center location."""
    body = 'https://nominatim.openstreetmap.org/search?'
    query = urllib.parse.urlencode([('format', 'json'), ('q', center_location)])
    return body + query


def reverse_geo_url(lat: float, lon: float) -> str:
    """Create URL for reverse geocoding given the coordinates."""
    body = 'https://nominatim.openstreetmap.org/reverse?'
    query = urllib.parse.urlencode([('lat', lat), ('lon', lon), ('format', 'json')])
    return body + query


def get_data_from_json(json_dict: dict) -> list:
    """Return the data field as a nested list from the dictionary."""
    return json_dict['data']


def get_lat_lon(data: list) -> list:
    """Get the latitude and longitude from the data from sensors."""
    lat_lon = [data[27], data[28]]
    return lat_lon


def second_input_line(command: str) -> int:
    """Get the range from the second line of input."""
    command_split = command.split()
    if command_split[0] == 'RANGE' and int(command_split[1]) > 0:
        range = int(command_split[1])
        return range


def third_input_line(command: str) -> int:
    """Get the threshold from the third line of input."""
    command_split = command.split()
    if command_split[0] == 'THRESHOLD' and int(command_split[1]) > 0:
        threshold = int(command_split[1])
        return threshold


def fourth_input_line(command: str) -> int:
    """Get the max number of entries from the fourth line of input."""
    command_split = command.split()
    if command_split[0] == 'MAX' and int(command_split[1]) > 0:
        max_Value = int(command_split[1])
        return max_Value



class ForwardGeoFile:
    def __init__(self, file_path = 'forward_geo.txt') -> None:
        self.file_path = file_path
    
    def get_data(self) -> list:
        json_data = file_data(self.file_path)
        return json_data



class ForwardGeoAPI:
    def __init__(self, location) -> None:
        self.location = location

    def get_data(self) -> list:
        url = forward_geo_url(self.location)
        json_data = api_data(url, 'forward_geo.txt')
        return json_data



class AQIfile:
    def __init__(self, file_path = 'aqi.txt') -> None:
        self.file_path = file_path
    
    def get_AQI(self) -> list:
        json_data = file_data(self.file_path)
        data = get_data_from_json(json_data)
        return data
    


class AQIpurpleAir:
    def __init__(self) -> None:
        self.url = PURPLEAIR_URL
    
    def get_AQI(self) -> list:
        json_data = api_data(self.url, 'aqi.txt')
        data = get_data_from_json(json_data)
        return data



class ReverseGeoPurpleAir:
    def __init__(self, data) -> None:
        self.data = data

    def get_reverse_data(self):
        locations = []
        for index, i in enumerate(self.data):
            try:
                location = get_lat_lon(i)
                url = reverse_geo_url(location[0], location[1])
                reverse_data = api_data(url, f'reverse_geo_data{index}')
                locations.append(reverse_data['display_name'])
            except:
                print('FAILED')
                print('https://nominatim.openstreetmap.org/reverse?')
                print('FORMAT')
        return locations



class ReverseGeoFile:
    def __init__(self, file_paths) -> None:
        self.file_paths = file_paths

    def get_reverse_data(self):
        locations = []
        for i in self.file_paths:
            reverse_data = file_data(i)
            locations.append(reverse_data['display_name'])
        return locations
