#!/usr/bin/env python3
'''
    api-test.py
    Jeff Ondich, 11 April 2016

    An example for CS 257 Software Design. How to retrieve results
    from an HTTP-based API, parse the results (JSON in this case),
    and manage the potential errors.
'''

import sys
import argparse
import json
import ssl
import urllib.request

# (1) get a list of things: category is either 'countries' or 'cities'
def get_names(category, location_name = None):
    location_data = get_decoded_data(category)
    name_key = get_name_key(category)
    location_names = []
    for location in location_data:
        location_names.append(location[name_key])
    if location_name is None:
        return location_names
    elif location_name in location_names:
        return [location_name]
    else:
        print("Invalid location name")
        return ''

def get_name_key(category):
    if category == 'countries':
        name_key = 'name'
    else:
        name_key = 'city'
    return name_key

# (2) get details about a single thing
def get_measurements(category, location_name = None):
    location_data = get_decoded_data(category)
    name_key = get_name_key(category)
    measurements = []
    if location_name is not None and location_name not in get_names(category):
        print("Invalid location name")
        return ''
    else:
        for location in location_data:
            if(location_name is None or location[name_key] == location_name):
                measurements.append([location[name_key], location['count']])
    return measurements

def get_decoded_data(category):
    data_from_server = get_data(category)
    string_from_server = data_from_server.decode('utf-8', errors="replace")
    decoded_data = json.loads(string_from_server)
    return decoded_data['results']

def get_data(category):
    base_url = 'https://api.openaq.org/v1/{0}'
    url = base_url.format(category)
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) # skips certification verificition
    data_from_server = urllib.request.urlopen(url, context=gcontext).read()
    return data_from_server

def main(args):
    if args.action == 'names':
        names = get_names(args.category, args.specific_location)
        for name in names:
            print(name)

    elif args.action == 'measurements':
        measurements_data = get_measurements(args.category, args.specific_location)
        for measurement in measurements_data:
            print(measurement[0], ":", measurement[1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get survey info from the Openaq API')

    parser.add_argument('action',
                        metavar='action',
                        help='the language as a 3-character ISO code',
                        choices=['names', 'measurements'])

    parser.add_argument('category',
                        metavar='category',
                        help='categories to examine: countries or cities',
                        choices=['countries', 'cities'])

    parser.add_argument('specific_location', nargs='?',
                        metavar='specific_location',
                        help='a specific city or country to look at')

    args = parser.parse_args()
    main(args)
