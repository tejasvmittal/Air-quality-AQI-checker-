import filter_and_calculate
import get_data

def print_lat_lon(lat: float, lon: float) -> list:
    """Print latitude and longitude along with the directional letter (N, S, E, W)."""
    final_lat = ''
    final_lon = ''
    if float(lat) < 0:
        final_lat = str(lat)[1:] + '/' + 'S'
    else:
        final_lat = str(lat) + '/' + 'N'
    if float(lon) < 0:
        final_lon = str(lon)[1:] + '/' + 'W'
    else:
        final_lon = str(lon) + '/' + 'E'
    return [final_lat, final_lon]


def print_center(center_lat: float, center_lon: float) -> None:
    """Print the first line of output."""
    formatted_lat_lon = print_lat_lon(center_lat, center_lon)
    print(f'CENTER {formatted_lat_lon[0]} {formatted_lat_lon[1]}')


def print_sensor_details(data: list, locations: list) -> None:
    """Print the information in the required format for the filtered sensors."""
    for i in range(len(data)):
        print(f'AQI {data[i][1]}')
        formatted_lat_lon = print_lat_lon(data[i][27], data[i][28])
        print(f'{formatted_lat_lon[0]} {formatted_lat_lon[1]}')
        print(locations[i])


def filter(data: list, threshold: int, range: int, center_lat: float, center_lon: float, max_: int) -> list:
    """Apply all the filter to the data and return the final data."""
    age_filter = filter_and_calculate.age_filter(data)
    outdoor_filter = filter_and_calculate.outdoor_filter(age_filter)
    range_filter = filter_and_calculate.range_distance(outdoor_filter, range, center_lat, center_lon)
    aqi_converted = filter_and_calculate.p_to_aqi(range_filter)
    threshold_filter = filter_and_calculate.threshold_filter(aqi_converted, threshold)
    final_data = filter_and_calculate.descending_and_max(threshold_filter, max_)
    return final_data


def main() -> None:
    """Ties everything together and gets all the information required for the project."""
    first_input = input()
    first_input_list = first_input.split()
    if first_input_list[1] == 'NOMINATIM':
        location = ' '.join(first_input_list[2:])
        data = get_data.ForwardGeoAPI(location).get_data()
    else:
        data = get_data.ForwardGeoFile(first_input_list[2]).get_data()
    center_lat = data[0]['lat']
    center_lon = data[0]['lon']
    second_input = input()
    range = get_data.second_input_line(second_input)
    third_input = input()
    threshold = get_data.third_input_line(third_input)
    fourth_input = input()
    max_info = get_data.fourth_input_line(fourth_input)
    fifth_input = input()
    fifth_input_list = fifth_input.split()
    sixth_input = input()
    sixth_input_list = sixth_input.split()
    if fifth_input_list[1] == 'PURPLEAIR':
        aqi_data = get_data.AQIpurpleAir().get_AQI()
    else:
        aqi_data = get_data.AQIfile(fifth_input_list[2]).get_AQI()
    final_data = filter(aqi_data, threshold, range, center_lat, center_lon, max_info)
    if sixth_input_list[1] == 'NOMINATIM':
        locations = get_data.ReverseGeoPurpleAir(final_data).get_reverse_data()
    else:
        file_paths = sixth_input_list[2:]
        locations = get_data.ReverseGeoFile(file_paths).get_reverse_data()
    print_center(center_lat, center_lon)
    print_sensor_details(final_data, locations)




if __name__ == '__main__':
    main()