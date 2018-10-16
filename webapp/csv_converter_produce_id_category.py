"""
Converter 1:
Funtions:
1.Take a csv
2.produce a simple csv with one collumn from the original csv
Bat-Orgil Batjargal
Oct-15, 2018

"""

import sys
import re
import csv


def get_category_ids_from_recent_grads_csv_file(csv_file_name):
    csv_file = open(csv_file_name, encoding='utf-8')
    reader = csv.reader(csv_file)
    category = {}
    ids_categories = []
    added_categories = []
    for row in reader:
        assert len(row) == 21
        if row[6] == 'Major_category':
            continue
        if row[6] not in added_categories:
            new_id = len(ids_categories)
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
    first_row = {'Major_category', 'category_id'}
    writer.writerow(first_row)
    for id_category in ids_categories:
        id_category_row = [id_category['id'], id_category['name']]
        writer.writerow(id_category_row)
    output_file.close()

if __name__ == '__main__':
    print("hi")
    ids_categories = get_category_ids_from_recent_grads_csv_file('recent-grads.csv')
    print("Yow")
    save_category_id_table(ids_categories, 'category_ids.csv')
    print("finished")
