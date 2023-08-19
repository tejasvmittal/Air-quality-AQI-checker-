# Air-quality-AQI-checker-
The program

The program will read a sequence of lines of input from the Python shell that configures its behavior, then generate and print some output consistent with that configuration. The general goal of the program is this: Given a "center" point, a range (in miles), and an AQI threshold, describe the locations within the given range of the center point having the n worst AQI values that are at least as much as the threshold.

The input

The program reads several lines of input that describe the job you want it to do. The input requirements are as follows:

The first line of input will be in one of two formats:
CENTER NOMINATIM location, where location is any arbitrary, non-empty string describing the "center" point of our analysis. For example, if this line of input said CENTER NOMINATIM Bren Hall, Irvine, CA, the center of our analysis is Bren Hall on the campus of UC Irvine. The word NOMINATIM indicates that we'll use Nominatim's API to determine the precise location (i.e., the latitude and longitude) of our center point.
CENTER FILE path, where path is the path to a file on your hard drive containing the result of a previous call to Nominatim. The file needs to exist. The expectation is the file will contain data in the same format that Nominatim would have given you, but will allow you to test your work without having to call the API every time — important, because Nominatim imposes limitations on how often you can call into it, and because this could allow you to make large parts of the program work without having hooked up the APIs at all.
The second line of input will be in the following format:
RANGE miles, where miles is a positive integer number of miles.
The third line of input will be in the following format:
THRESHOLD AQI, where AQI is a positive integer specifying the AQI threshold, which means we're interested in finding places that have AQI values at least as high as that threshold.
The fourth line of input will be in the following format:
MAX number, where number is the maximum number of locations we want to find in our search.
The fifth line of input will be in one of two formats:
AQI PURPLEAIR, which means that we want to obtain our air quality information from PurpleAir's API.
AQI FILE path, where path is the path to a file on your hard drive containing the result of a previous call to PurpleAir's API with all of the sensor data in it.
The sixth line of input will be in one of two formats:
REVERSE NOMINATIM, which means that we want to use the Nominatim API to do reverse geocoding, i.e., to determine a description of where problematic air quality sensors are located.
REVERSE FILES path1 path2 ..., which means that we want to use files stored on our hard drive containing the results of previous calls to Nominatim's reverse geocoding API instead. Paths are separated by spaces — which means they can't contain spaces — and we expect there to be at least as many paths listed as the number we passed to MAX (e.g., if we said MAX 5 previously, then we'd specify at least five files containing reverse geocoding data).

The output

After reading all of the input, the program displays the latitude and longitude of the center location, with latitudes and longitudes shown in the following format.

CENTER 33.64324045/N 117.84185686276017/W
Then it uses the information that's either stored in the specified files or downloaded from the specified APIs to find the sensors that are in the specified range of the center location, then determines which of those sensors have the highest AQI values and, for any of them that are at or above the AQI threshold, display information about the first n of them. For example, suppose the input was as follows:

CENTER NOMINATIM Bren Hall, Irvine, CA
RANGE 30
THRESHOLD 150
MAX 5
AQI PURPLEAIR
REVERSE NOMINATIM
This means we're looking for up to five locations within 30 miles of Bren Hall at UC Irvine where the AQI value is at least 150. Given a choice (i.e., if there are more than five locations with AQI values that meet the threshold), we want to show information about the five locations with the highest AQI values. The program displays these in descending order of their AQI. For each location, the program prints three lines of output:

AQI AQI_value, where AQI_value is the AQI value you calculated for this location.
latitude longitude, which is the latitude and longitude for this location, in the same format as it prints the center location's latitude and longitude.
description, which is the full description of the location.
