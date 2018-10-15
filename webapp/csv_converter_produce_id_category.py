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


def load_from_books_csv_file(csv_file_name):
    csv_file = open(csv_file_name, encoding='utf-8')
    reader = csv.reader(csv_file)

    category = {}
    ids_categories = []
    for row in reader:
        assert len(row) == 21

        if row[6] not in ids_categories.values():
            new_id = len(ids_categories)
            category = {'id': new_id, 'name': row[6]}
            print(category)
            ids_categories.append(category)
    csv_file.close()
    return (ids_categories)

def save_linking_table(ids_categories, csv_file_name):
    ''' Save the books in CSV form, with each row containing
        (book id, author id). '''
    output_file = open(csv_file_name, 'w', encoding='utf-8')
    writer = csv.writer(output_file)
    for id_category in ids_categories:
        id_category_row = [id_category['id'], id_category['name']]
        writer.writerow(id_category_row)
    output_file.close()


if __name__ == '__main__':
    print("hi")
    ids_categories = load_from_books_csv_file('recent-grads.csv')
    print("Yow")
    save_linking_table(ids_categories, 'books_authors.csv')
    print("finished")
