#Alec Wang and Bat-Orgil Batjargal

#methods that we will use on the api - CareerSalaryDataSource

import re
import csv
import sys
import flask
import json
import psycopg2
from config_alec import password
from config_alec import database
from config_alec import user
import collections

app = flask.Flask(__name__)

@app.route('/')
def hello():
    # Connect to the database
    return("Hello! Welcome to Bat and Alec's API."
                + "Use query strings in the URL: cat=category_id, min_sal=minimum_salary,"
                + "maj=major_search_text, sort=sort_by, lim=limit."
                + "You can sort by any dictionary key in a major."
                + "If you want to search by percent instead of raw numbers, use 'percent_key' (i.e. 'percent_women'). Enjoy!")

@app.route('/majors')
def get_majors(category_id = None, minimum_salary = None, major_contains = None, sort_by = None, limit = None):
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    user_parameters = get_user_parameters(category_id, minimum_salary, major_contains, sort_by, limit)
    sql_query = get_sql_query(user_parameters)
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
    except Exception as e:
        print(e)
        exit()
    categories = get_category_id_pairs(connection)
    if(user_parameters['sort_by'] != None):
        majors = get_list_of_sorted_majors(cursor, user_parameters, categories)
    else:
	    majors = get_list_of_unsorted_majors(cursor, categories)
    return json.dumps(majors)
    connection.close()

def get_user_parameters(category_id, minimum_salary, major_contains, sort_by, limit):
    if (flask.request.args.get('cat')):
        category_id = flask.request.args.get('cat')
    if (flask.request.args.get('min_sal')):
        minimum_salary  = flask.request.args.get('min_sal')
    if (flask.request.args.get('maj')):
        major_contains = flask.request.args.get('maj')
    if (flask.request.args.get('sort')):
        sort_by = flask.request.args.get('sort')
    if (flask.request.args.get('lim')):
        limit = flask.request.args.get('lim')
    user_parameters = {'category_id': category_id,
                 'median': minimum_salary,
                 'major_contains': major_contains,
                 'sort_by': sort_by,
                 'limit': limit}
    return user_parameters

def get_sql_query(user_parameters):
    query_where_clause = get_query_where_clause(user_parameters)
    query = 'SELECT * FROM majors ' + query_where_clause
    return(query)

def get_query_where_clause(arguments):
    where_clause = ' '
    if arguments['category_id'] != None or arguments['median'] != None or arguments['major_contains'] != None:
        where_clause = where_clause + 'WHERE '
    if arguments['category_id'] != None:
        where_clause = where_clause + 'category_id = ' + arguments['category_id'] + ' AND '
    if arguments['median'] != None:
        where_clause = where_clause + 'median > ' + arguments['median'] + ' AND '
    if arguments['major_contains'] != None:
        where_clause = where_clause + "major LIKE '%" + arguments['major_contains'].upper() + "%' AND "
    if (len(where_clause) > 0):
        where_clause = where_clause[:-5] # remove extra ' AND '
    if arguments['limit'] != None:
        where_clause = where_clause + 'LIMIT ' + arguments['limit']
    return(where_clause)

def get_major_dictionary(row, categories):
    data_types = ["id", "major", "total", "men", "women", "category_id", "employed", "full_time", "part_time", "unemployed",
            "median", "p25th", "p75th", "college_jobs",  "non_college_jobs", "low_wage_jobs"]
    major = collections.OrderedDict()
    index = 0
    for cell in row:
        data_type = data_types[index]
        major[data_type] = str(cell)
        if(data_type == "unemployed"):
            unemployment_rate = get_unemployment_rate(row)
            major["unemployment_rate"] = unemployment_rate
        index = index + 1
    major = replace_category_id_with_category(major, categories)
    return major

def get_unemployment_rate(row):
    total = row[2]
    unemployed = row[9]
    if(total is not None and unemployed is not None):
        unemployment_rate = str(int(unemployed)/int(total))
    else:
        unemployment_rate = "NULL"
    return unemployment_rate

def replace_category_id_with_category(major, categories):
    category_id = major["category_id"]
    major["category"] = categories[int(category_id)]
    major.pop("category_id", None)
    return major

def get_category_id_pairs(connection):
    sql_query = 'SELECT * FROM categories'
    categories = {}
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
    except Exception as e:
        print(e)
        exit()
    for row in cursor:
        id = row[0]
        category = row[1]
        categories[id] = category
    return categories

def get_list_of_unsorted_majors(cursor, categories):
    majors = []
    for row in cursor:
        major = get_major_dictionary(row, categories)
        majors.append(major)
    return majors

def get_list_of_sorted_majors(cursor, arguments, categories):
    # Every major is linked with a key called an "order key"
    # The order keys are sorted and then the majors are retrieved
    # in the order of their matching keys.
    majors_order_key_pairs = {}
    sort_type = arguments['sort_by']
    print('sort_type:' + sort_type)
    for row in cursor:
        major = get_major_dictionary(row, categories)
        order_key = get_order_key(major, sort_type)
        print('order_key:' + order_key)
        majors_order_key_pairs[order_key] = major
    majors_keys_sorted_descending = sorted(majors_order_key_pairs, reverse=True)
    majors = []
    for key in majors_keys_sorted_descending:
        majors.append(majors_order_key_pairs[key])
    return majors

def get_order_key(major, sort_type):
    if sort_type in ('percent_men', 'percent_women', 'percent_employed', 'percent_full_time', 'percent_part_time',
                     'percent_unemployed', 'percent_employed', 'percent_college_jobs', 'percent_non_college_jobs',
                     'percent_low_wage_jobs'):
        order_key = get_order_key_as_percent(major, sort_type[8:])
        print('percent;')
    else:
        order_key = get_order_key_as_numeric(major, sort_type)
    print(order_key)
    return order_key

def get_order_key_as_percent(major, dividend):
    try:
        return int(major[dividend])/int(major['total'])
    except:
        return 0

def get_order_key_as_numeric(major, sort_type):
    order_key = major[sort_type]
    if(order_key == 'None' or order_key == 'NULL' or order_key is None):
        return 0
    else:
        int(order_key)
        return order_key

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5126'.format(sys.argv[0]))
        exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)


	# csv_file = open(recent-grads-category-ids.csv, encoding='utf-8')
    # reader = csv.reader(csv_file)
    # to_return = []
	#
    # if category_id:
    #     for row in reader:
    #         if row[6] == category_id:
    #         	to_return.add(row)
    # if major_contains:
    # 	for item in to_return:
    # 		if item[2] not in major_contains.lower():
    # 			to_return.remove(item)
    # if minimum_salary:
    # 	for item in to_return:
    # 		if item[15] < minimum_salary
    # 			to_return(x)
    # if to_return.len() > limit:
    # 	to_return = to_return[0:limit-1]
	#
    # if sort_by:
	#
	#
    # return (to_return)
	#




	#Get a list of all the undergraduate majors
	#try to get the data and loop and add them into a list then print
