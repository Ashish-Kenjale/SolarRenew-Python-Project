# google.py
# Authors - Jonika Rathi, Shubhang Seth
# This is the program utility used to integrate with Google's Geo-coding APIs.
# This file is imported by main.py

# It uses requests module to make an API request
import requests


# Function to extract the zipcode and state from the json response
def get_zipcode_and_state(res):
    result = {}
    for item in res[0]['address_components']:
        for type in item['types']:
            if type == 'postal_code':
                result[type] = item['long_name']
            elif type == 'administrative_area_level_1':
                result['state'] = item['long_name']
    return result


# Use this function to get coordinates for an address
def get_coordinates(address):
    google_url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyCEieeIKvqlFjZsdJL0mp2cgL2gFZMsbWM' + \
                 '&address=' + address
    response = requests.get(google_url)

    if response.status_code == 200:
        # We have a successful response here. Let's extract the data we need
        res = response.json()

        # We expect the user to enter full address with city. Hence the expected output is a single element in the json
        # result array. Even if there are multiple, we assume the first is what we want
        result = get_zipcode_and_state(res['results'])
        result['location'] = res['results'][0]['geometry']['location']
        return result


# This is for testing purpose only
if __name__ == "__main__":
    print(get_coordinates('5516 Bartlett St, Pittsburgh'))
