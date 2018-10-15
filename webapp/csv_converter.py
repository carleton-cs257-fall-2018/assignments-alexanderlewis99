#!/usr/bin/env python3

'''
    csv_converter
    Alec Wang, October 13, 2018
    Bat-Orgil Batjargal
'''

import sys
import re
import csv

def load_from_majors_csv_file(recent_grads_csv, category_numbers_csv):
    #opens recent_grads_csv
    majors_csv_file = open(recent_grads_csv)
    majors_csv_reader = csv.reader(majors_csv_file)

    #opens output_file.csv
    output_file = open("output_file.csv", 'w')
    writer = csv.writer(output_file)

    #opens category_numbers_csv
    category_numbers_csv_file = open(category_numbers_csv)
    category_numbers_csv_reader = csv.reader(category_numbers_csv_file)

    category_numbers = {}
    for row in category_numbers_csv_reader:
        if row[0] not in category_numbers.keys():
            category_numbers[row[1]] = row[0]
    print(category_numbers)

    for row in majors_csv_reader:
        new_row = [category_numbers[row[6]], row[6]]
        writer.writerow(new_row)
    majors_csv_file.close()
    output_file.close()

load_from_majors_csv_file("recent-grads.csv", "category_numbers.csv")
