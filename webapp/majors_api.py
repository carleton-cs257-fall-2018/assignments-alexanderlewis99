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

@app.route('/majors/')
def get_majors(category_id = None, minimum_salary = None, major_contains = None, sort_by = None, limit = None):
    connection = get_connection_to_server()
    categories = get_category_id_pairs(connection)
    user_parameters = get_user_parameters(category_id, minimum_salary, major_contains, sort_by, limit, categories)
    sql_query = get_sql_query(user_parameters)
    cursor = get_data_from_server(connection, sql_query)
    if(user_parameters['sort_by'] is not None):
        majors = get_list_of_sorted_majors(cursor, user_parameters, categories)
    else:
	    majors = get_list_of_unsorted_majors(cursor, categories)
    majors = reduce_number_of_majors_to_limit(majors, user_parameters['limit'])
    resp = flask.Response(json.dumps(majors))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    connection.close()
    return resp

def get_connection_to_server():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    return connection

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

def get_data_from_server(connection, sql_query):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
    except Exception as e:
        print(e)
        exit()
    return cursor

def reduce_number_of_majors_to_limit(majors, limit):
    if(limit is not None):
        print("IS LIMIT IS LIMIT IS LIMIT")
        while len(majors) > limit:
            majors.pop()
    return majors

def get_category_id(categories, input_category):
    input_category = input_category.lower().replace("%20", "").replace("and", "&").replace(" ", "")
    categories_reversed = {}
    for id in range(1, len(categories) + 1):
        category = categories[id].lower().replace(" ", "")
        categories_reversed[category] = id
    return categories_reversed[input_category]

def get_user_parameters(category_id, minimum_salary, major_contains, sort_by, limit, categories):
    if (flask.request.args.get('cat')):
        input_category = flask.request.args.get('cat')
        category_id = get_category_id(categories, input_category)
    if (flask.request.args.get('min_sal')):
        minimum_salary  = int(flask.request.args.get('min_sal'))
    if (flask.request.args.get('maj')):
        major_contains = flask.request.args.get('maj')
    if (flask.request.args.get('sort')):
        sort_by = flask.request.args.get('sort')
    if (flask.request.args.get('lim')):
        limit = int(flask.request.args.get('lim'))
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
        where_clause = where_clause + 'category_id = ' + str(arguments['category_id']) + ' AND '
    if arguments['median'] != None:
        where_clause = where_clause + 'median > ' + str(arguments['median']) + ' AND '
    if arguments['major_contains'] != None:
        where_clause = where_clause + "major LIKE '%" + arguments['major_contains'].upper() + "%' AND "
    if (len(where_clause) > 0):
        where_clause = where_clause[:-5] # remove extra ' AND '
    return(where_clause)

def get_major_dictionary(row, categories):
    data_types = ["id", "major", "total", "men", "women", "category_id", "employed", "full_time", "part_time", "unemployed",
            "median", "p25th", "p75th", "college_jobs",  "non_college_jobs", "low_wage_jobs"]
    major = collections.OrderedDict()
    index = 0
    for cell in row:
        data_type = data_types[index]
        major = add_cell_data_to_major(major, cell, data_type, row, categories, data_types)
        index = index + 1
    return major

def add_cell_data_to_major(major, cell, data_type, row, categories, data_types):
    if cell is None:
        major[data_type] = "NULL"
    elif data_type == "major":
        major[data_type] = str(cell)
    else:
        major[data_type] = int(cell)
    if(data_type == "men"):
        percent_men = get_percent_from_data(row, "men", data_types)
        major["percent_men"] = percent_men
    elif(data_type == "women"):
        percent_women = get_percent_from_data(row, "women", data_types)
        major["percent_women"] = percent_women
    elif(data_type == "employed"):
        percent_employed = get_percent_from_data(row, "employed", data_types)
        major["percent_employed"] = percent_employed
    elif(data_type == "full_time"):
        percent_full_time = get_percent_from_data(row, "full_time", data_types)
        major["percent_full_time"] = percent_full_time
    elif(data_type == "part_time"):
        percent_part_time = get_percent_from_data(row, "part_time", data_types)
        major["percent_part_time"] = percent_part_time
    elif(data_type == "unemployed"):
        unemployment_rate = get_percent_from_data(row, "unemployed", data_types)
        major["unemployment_rate"] = unemployment_rate
    elif(data_type == "college_jobs"):
        percent_college_jobs = get_percent_from_data(row, "college_jobs", data_types)
        major["percent_college_jobs"] = percent_college_jobs
    elif(data_type == "non_college_jobs"):
        percent_non_college_jobs = get_percent_from_data(row, "non_college_jobs", data_types)
        major["percent_non_college_jobs"] = percent_non_college_jobs
    elif(data_type == "low_wage_jobs"):
        percent_low_wage_jobs = get_percent_from_data(row, "low_wage_jobs", data_types)
        major["percent_low_wage_jobs"] = percent_low_wage_jobs
    elif data_type == "category_id":
        major = replace_category_id_with_category(major, categories)
    return major

def get_percent_from_data(row, data_type, data_types):
    total = row[2]
    number = row[data_types.index(data_type)]
    if(total is not None and number is not None and not number == 'NULL'):
        percent = float(int(number)/int(total))
    else:
        percent = "NULL"
    return percent

def replace_category_id_with_category(major, categories):
    category_id = major["category_id"]
    major["category"] = categories[int(category_id)]
    major.pop("category_id", None)
    return major

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
    for row in cursor:
        major = get_major_dictionary(row, categories)
        order_key = get_order_key(major, sort_type)
        majors_order_key_pairs[order_key] = major
    print(majors_order_key_pairs.keys())
    majors_keys_sorted_descending = sorted(majors_order_key_pairs, reverse=True)
    print(majors_keys_sorted_descending)
    majors = []
    for key in majors_keys_sorted_descending:
        majors.append(majors_order_key_pairs[key])
        if(key==0):
            print(majors_order_key_pairs[key])
    return majors

def get_order_key(major, sort_type):
    order_key = major[str(sort_type)]
    if(order_key == 'None' or order_key == 'NULL' or order_key is None):
        print(major["major"] + "0")
        return 0
    elif sort_type in ("major", "category"):
        return str(order_key)
    elif sort_type in ("unemployment_rate", "percent_men", "percent_women", "percent_employed", "percent_full_time", "percent_part_time",
                     "percent_unemployed", "percent_college_jobs", "percent_non_college_jobs", "percent_low_wage_jobs"):
        return float(order_key)
    else:
        return int(order_key)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5126'.format(sys.argv[0]))
        exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)
