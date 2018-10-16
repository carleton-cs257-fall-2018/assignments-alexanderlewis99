#!/usr/bin/env python3

'''
    csv_converter
    Alec Wang, October 13, 2018
    Bat-Orgil Batjargal
'''

import sys
import re
import csv

def get_category_ids(category_ids_csv):
    #opens category_numbers_csv
    category_ids_csv_file = open(category_ids_csv)
    category_ids_csv_reader = csv.reader(category_ids_csv_file)
    category_ids = {}
    for row in category_ids_csv_reader:
        category = row[1]
        id = row[0]
        if category not in category_ids.keys():
            category_ids[category] = id
    category_ids_csv_file.close()
    return(category_ids)

def write_recent_grads_csv_with_category_ids(recent_grads_csv, category_ids):
    #opens recent_grads_csv
    majors_csv_file = open(recent_grads_csv)
    majors_csv_reader = csv.reader(majors_csv_file)
    #opens output_file.csv
    output_file = open("recent-grads-category-ids.csv", 'w')
    writer = csv.writer(output_file)
    for row in majors_csv_reader:
        new_row = row
        new_row[6] = category_ids[row[6]]
        writer.writerow(new_row)
    majors_csv_file.close()
    output_file.close()

if __name__ == '__main__':
    category_ids = get_category_ids("category_ids.csv")
    write_recent_grads_csv_with_category_ids("recent-grads.csv", category_ids)
