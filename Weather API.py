"""
DSC 510
Week 12
Assignment Number: 12.1 Programming Assignment
Author: Saron Yaya
Date: June 2, 2023
Description:  This is an application that interacts with a webservice to obtain weather forecast data.

"""

import requests
import json

# ANSI escape sequence for red color
RED_COLOR = "\033[91m"

api_key = '95f734dbd5db989a8dca02b0bf824998'


def main():
    while True:
        try:
            # Prompt the user to request a response or quit
            make_request = input('Would you like to make a request? (Y/N): ')
            if make_request.lower() == 'y':
                # Prompt the user to choose between zip code or city
                city_zip = input('Would you like to lookup by zip code or by city? (zip/city): ')
                if city_zip.lower() == 'zip':
                    zip_lookup()  # Call the zip lookup function
                elif city_zip.lower() == 'city':
                    city_lookup()  # Call the city lookup function
                else:
                    print_error('Invalid Input. Please try again.')  # Print error if wrong input is entered
                    continue
            elif make_request.lower() == 'n':
                print('\nThank you for using my program!')  # End the program if user chooses quit
                break
            else:
                print_error('Invalid input. Please try again.')
                continue
        except ValueError:
            print_error('Invalid input. Please try again.')
            continue


def zip_lookup():
    try:
        # Prompt user to enter zip code and country code and call GEOCODE Lookup
        zip_code = input('Please enter zip code: ')
        country_code = input('Please enter the country code: ')
        geo_lookup_by_zip(zip_code, country_code)
    # Handle ValueError and KeyError
    except (ValueError, KeyError) as e:
        print_error(f'Error: {str(e)}')
        print_error('Please try again')


def city_lookup():
    try:
        # Prompt user to enter city, state, and country code and call GEOCODE Lookup
        while True:
            city = input('Please enter city: ')
            state = input('If US, Please enter the state: ')
            country_code = input('Please enter the country code: ')
            # Require state input if country is US
            if country_code.lower() == 'us' and state == '':
                print_error('State is required for US. Please try again.')
                continue
            else:
                geo_lookup_by_city(city, state, country_code)
                break
    # Handle ValueError and KeyError
    except (ValueError, KeyError) as e:
        print_error(f'Error: {str(e)}')
        print_error('Please try again')


def geo_lookup_by_zip(zip_code, country_code=''):
    try:
        # Prepare the API request
        url = f'https://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key}'
        headers = {'cache-control': 'no-cache'}
        response = requests.get(url, headers=headers)
        # Parse the json response and get lat and lon values
        data = json.loads(response.text)
        lon = data['lon']
        lat = data['lat']

        #  Get and show the user the city and country that is being looked up form GEO Lookup
        country = data['country']
        city_name = data['name']

        print(f'Getting weather data for {city_name}, {country}...')

        weather_lookup(lat, lon)

    # Using requests.exceptions.RequestException to handle exceptions such as ConnectionError, Timeout, HTTPError, etc.
    except requests.exceptions.RequestException as e:
        print_error(f'Request Error: {str(e)}')
        print_error('Please try again')
    # Handle JSONDecodeError
    except requests.exceptions.JSONDecodeError as e:
        print_error(f'Request Error: {str(e)}')
        print_error('Please try again')
    # Handle ValueError
    except ValueError as e:
        print_error(f'Error: {str(e)}')
        print_error('Please try again')
    # Handle KeyError
    except KeyError as e:
        print_error(f'Error: Key {str(e)} not found in response data. ')
        print_error('Please try again')


def geo_lookup_by_city(city, state, country_code=''):
    try:
        # Prepare the API request
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country_code}&appid={api_key}'
        headers = {'cache-control': 'no-cache'}
        response = requests.get(url, headers=headers)
        # Parse the json response
        data = json.loads(response.text)
        #  If response is not empty get the lat and lon values and call weather lookup API
        if data:
            location = data[0]  # Access the first location in the list
            lon = location['lon']
            lat = location['lat']

            #  Get and show the user the city, state, and country that is being looked up form GEO Lookup
            city_name = location['name']
            state_name = location['state']
            country = location['country']
            print(f'Getting weather data for {city_name},{state_name}, {country}...')

            weather_lookup(lat, lon)
        else:
            print_error('Invalid input. Please try again.')

    # Using requests.exceptions.RequestException to handle exceptions such as ConnectionError, Timeout, HTTPError, etc.
    except requests.exceptions.RequestException as e:
        print_error(f'Request Error: {str(e)}')
        print_error('Please try again')
    # Handle JSONDecodeError
    except requests.exceptions.JSONDecodeError as e:
        print_error(f'Request Error: {str(e)}')
        print_error('Please try again')
    # Handle ValueError
    except ValueError as e:
        print_error(f'Error: {str(e)}')
        print_error('Please try again')
    # Handle KeyError
    except KeyError as e:
        print_error(f'Error: Key {str(e)} not found in response data. ')
        print_error('Please try again')


def weather_lookup(lat, lon):
    try:
        # Prompt user to choose the unit
        unit = input('Would you like to see the temperature in Celsius, Fahrenheit, or Kelvin (C/F/K): ')
        if unit.lower() in ['fahrenheit', 'f']:
            units = 'imperial'
            unit_symbol = '°F'
        elif unit.lower() in ['celsius', 'c']:
            units = 'metric'
            unit_symbol = '°C'
        elif unit.lower() in ['kelvin', 'k']:
            units = 'standard'
            unit_symbol = 'K'
        else:
            units = 'imperial'
            unit_symbol = '°F'

        # Prepare the API request
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={api_key}'
        headers = {'cache-control': 'no-cache'}
        response = requests.get(url, headers=headers)

        # Call the print function to display the response
        print_weather_response(response, unit_symbol)

    # Using requests.exceptions.RequestException to handle exceptions such as ConnectionError, Timeout, HTTPError, etc.
    except requests.exceptions.RequestException as e:
        print_error(f'Request Error: {str(e)}')
        print_error('Please try again')
    # Handle JSONDecodeError
    except requests.exceptions.JSONDecodeError as e:
        print_error(f'Request Error: {str(e)}')
        print_error('Please try again')
    # Handle ValueError
    except ValueError as e:
        print_error(f'Error: {str(e)}')
        print_error('Please try again')
    # Handle KeyError
    except KeyError as e:
        print_error(f'Error: Key {str(e)} not found in response data. ')
        print_error('Please enter the correct input and try again')


def print_weather_response(response, unit_symbol):
    data = response.json()
    # Get the values of the keys from the response
    main_value = data['main']
    clouds = data["weather"][0]["description"]
    temp = main_value['temp']
    feels_like = main_value['feels_like']
    temp_min = main_value['temp_min']
    temp_max = main_value['temp_max']
    pressure = main_value['pressure']
    humidity = main_value['humidity']

    # Display the output in a readable format
    print(f'\nTemperature: {temp:.2f} {unit_symbol}')
    print(f'Feels Like: {feels_like:.2f} {unit_symbol}')
    print(f'High Temperature: {temp_min:.2f} {unit_symbol}')
    print(f'Low Temperature: {temp_max:.2f} {unit_symbol}')
    print(f'Pressure: {pressure}')
    print(f'Humidity: {humidity}%')
    print(f'Clouds: {clouds}\n')


# Function that gets called for error messages to be displayed in red
def print_error(message):
    print(f'{RED_COLOR}{message}\033[0m')


if __name__ == '__main__':
    main()


# Change Control Log:
# Date (MM-DD-YYYY)  |   Author   |   Description of Change
# -------------------|------------|-----------------------------
# 05-10-2023         | Saron Yaya | Initial version of program
# 06-02-2023         | Saron Yaya | Final version of program
