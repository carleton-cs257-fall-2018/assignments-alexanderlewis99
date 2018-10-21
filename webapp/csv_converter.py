#!/usr/bin/env python3

'''
    csv_converter
    Alec Wang, October 13, 2018
    Bat-Orgil Batjargal, Oct-15, 2018
'''

import sys
import re
import csv

def get_category_ids(majors_csv_file_name):
    """
    Produces a csv mapping category with an ID
    """
    majors_csv_file = open(majors_csv_file_name, encoding='utf-8')
    majors_reader = csv.reader(majors_csv_file)
    category_ids = {}
    for row in majors_reader:
        assert len(row) == 21
        category = row[6]
        id = len(category_ids)
        if category not in category_ids.keys():
            if category == 'Major_category':
                id = 'category_id'
            category_ids[category] = id
    majors_csv_file.close()
    return (category_ids)

def get_majors_csv_data(recent_grads_csv):
    #opens recent_grads_csv
    majors_csv_file = open(recent_grads_csv)
    majors_csv_reader = csv.reader(majors_csv_file)
    majors_data = []
    for row in majors_csv_reader:
        majors_data.append(row)
    majors_csv_file.close()
    return (majors_data)

def replace_majors_csv_data_categories_with_ids(majors_data, category_ids):
    for row in majors_data:
        row[6] = category_ids[row[6]]
    return majors_data

def remove_headers_from_majors_csv(majors_data):
    majors_data.pop(0) # removes first row
    return majors_data

def remove_unwanted_columns_from_majors_csv(majors_data):
    for row in majors_data:
        row.pop(14) #unemployment_rate
        row.pop(12) #full_time_year_round
        row.pop(8) #sample_size
        row.pop(7) #sharewomen
        row.pop(1) #major_code
        row.pop(0) #rank
    return majors_data

def make_serials_in_place_of_rank(majors_data):
    serial_id = 0
    for row in majors_data:
        row[0] = serial_id
        serial_id = serial_id + 1
    return majors_data

def replace_empty_data_with_null(majors_data):
    row_index = 0
    cell_index = 0
    for row in majors_data:
        for cell in row:
            if cell == "":
                majors_data[row_index][cell_index] = "NULL"
            cell_index = cell_index + 1
        row_index = row_index + 1
        cell_index = 0
    return majors_data

def save_category_id_table(category_ids):
    ''' Save the category_ids in CSV form, with each row containing
        (category id, category name). '''
    output_file = open('category-ids.csv', 'w', encoding='utf-8')
    writer = csv.writer(output_file)
    category_ids.pop('Major_category', None)
    for category in category_ids.keys():
        row = [category_ids[category], category]
        writer.writerow(row)
    output_file.close()

def save_majors_table(majors_data):
    output_file = open('recent-grads-db-ready.csv', 'w', encoding='utf-8')
    writer = csv.writer(output_file)
    for row in majors_data:
        writer.writerow(row)
    output_file.close()

if __name__ == '__main__':
    category_ids = get_category_ids('recent-grads.csv')
    majors_data = get_majors_csv_data("recent-grads.csv")
    majors_data = replace_majors_csv_data_categories_with_ids(majors_data, category_ids)
    majors_data = remove_headers_from_majors_csv(majors_data)
    majors_data = remove_unwanted_columns_from_majors_csv(majors_data)
    majors_data = replace_empty_data_with_null(majors_data)
    majors_data = make_serials_in_place_of_rank(majors_data)
    save_category_id_table(category_ids)
    save_majors_table(majors_data)
