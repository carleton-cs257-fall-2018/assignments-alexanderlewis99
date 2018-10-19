#!/usr/bin/env python3

'''
    csv_converter
    Alec Wang, October 13, 2018
    Bat-Orgil Batjargal, Oct-15, 2018
'''

import sys
import re
import csv

def get_ids_for_categories(csv_file_name):
    """
    Produces a csv mapping category with an ID
    """
    csv_file = open(csv_file_name, encoding='utf-8')
    reader = csv.reader(csv_file)
    category = {}
    ids_categories = []
    added_categories = []
    for row in reader:
        assert len(row) == 21
        if row[6] not in added_categories:
            new_id = len(ids_categories)
            if row[6] == 'Major_category':
                new_id = 'category_id'
            category = {'id': new_id, 'name': row[6]}
            ids_categories.append(category)
            added_categories.append(row[6])
    csv_file.close()
    return (ids_categories)

def save_category_id_table(ids_categories, csv_file_name):
    ''' Save the category_ids in CSV form, with each row containing
        (category id, category name). '''
    output_file = open(csv_file_name, 'w', encoding='utf-8')
    writer = csv.writer(output_file)
    for id_category in ids_categories:
        id_category_row = [id_category['id'], id_category['name']]
        writer.writerow(id_category_row)
    output_file.close()

def get_category_ids(category_ids_csv):
    #opens category_numbers_csv
    category_ids_csv_file = open(category_ids_csv)
    category_ids_csv_reader = csv.reader(category_ids_csv_file)
    category_ids = {}
    for row in category_ids_csv_reader:
        category = row[1]
        id = row[0]
        key = category
        value = id
        if category not in category_ids.keys():
            category_ids[key] = value
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

def remove_columns_and_headers(recent_grads_csv):
    #opens recent_grads_csv
    majors_csv_file = open(recent_grads_csv)
    majors_csv_reader = csv.reader(majors_csv_file)
    #opens output_file.csv
    output_file = open("recent-grads-db-ready.csv", 'w')
    writer = csv.writer(output_file)
    first_row = True
    for row in majors_csv_reader:
        if(first_row):
            first_row = False
            continue
        new_row = row
        new_row.pop(14) #unemployment_rate
        new_row.pop(12) #full_time_year_round
        new_row.pop(8) #sample_size
        new_row.pop(7) #sharewomen
        new_row.pop(1) #major_code
        #new_row.pop(0) #rank
        writer.writerow(new_row)
    majors_csv_file.close()
    output_file.close()

def remove_category_ids_headers(category_ids_csv):
    #opens category_ids_csv
    category_ids_csv_file = open(category_ids_csv)
    category_ids_csv_reader = csv.reader(category_ids_csv_file)
    #opens output_file.csv
    output_file = open("category-ids-db-ready.csv", 'w')
    writer = csv.writer(output_file)
    first_row = True
    for row in category_ids_csv_reader:
        if(first_row):
            first_row = False
            continue
        new_row = row
        writer.writerow(new_row)
    category_ids_csv_file.close()
    output_file.close()

if __name__ == '__main__':
    ids_categories = get_ids_for_categories('recent-grads.csv')
    save_category_id_table(ids_categories, 'category-ids.csv')
    category_ids = get_category_ids("category-ids.csv")
    write_recent_grads_csv_with_category_ids("recent-grads.csv", category_ids)
    remove_columns_and_headers("recent-grads-category-ids.csv")
    remove_category_ids_headers("category-ids.csv")
