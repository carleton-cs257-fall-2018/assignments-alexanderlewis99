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
    text_to_return = ""
    text_to_return = text_to_return + 'Hello!'
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        text_to_return + e
        exit()
    try:
        cursor = connection.cursor()
        sql_query = 'SELECT * FROM majors'
        cursor.execute(sql_query)
        for row in cursor:
            text_to_return = text_to_return + ('===== Majors =====')
            text_to_return = text_to_return + row[1]
        return(text_to_return)
    except Exception as e:
        text_to_return = text_to_return + ":( It didn't work"
        text_to_return = text_to_return + e
        return(text_to_return)
        exit()



@app.route('/majors')
def get_majors(category_id = None, minimum_salary = None, major_contains = None, sort_by = None, limit = None):
    arguments = get_url_query_string_args(category_id, minimum_salary, major_contains, sort_by, limit)
    sql_query_requirements = get_query_requirements(arguments)
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        text_to_return + e
        exit()

    sql_query = 'SELECT * FROM majors' + sql_query_requirements
    print(sql_query)

    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)

    except Exception as e:
        print(e)
        exit()
    #percent woman and percent man calculation for each major
    #for row in cursor:
        #tell me by what to sort and call it X
        #find the percent of X
        #add it into the end of cursor
        #write a sql Query - order by the new added column in the each row in the end
        #cursor.execute(new SQL query )
    print(arguments['sort_by'])
    if(arguments['sort_by'] != None):
        majors = get_list_of_sorted_majors(cursor, arguments)
    else:
	       majors = get_list_of_unsorted_majors(cursor)
    return json.dumps(majors)
    # Don't forget to close the database connection.
    connection.close()

def get_list_of_unsorted_majors(cursor):
    majors = []
    for row in cursor:
        major = get_major_dictionary(row)
        majors.append(major)
    return majors

def get_list_of_sorted_majors(cursor, arguments):
    majors_sort_key_pairs = {}
    for row in cursor:
        major = get_major_dictionary(row)
        if arguments['sort_by'] in ('men', 'women', 'employed, full_time', 'part_time', 'unemployment_rate', 'employed',
                'college_jobs', "non_college_jobs", "low_wage_jobs"):
            sort_key = get_sort_key_percent(major, arguments['sort_by'])
        else:
            sort_key = arguments['sort_by']
        print(sort_key)
        majors_sort_key_pairs[sort_key] = major
    majors = sorted(majors_sort_key_pairs)
    return majors

def get_major_dictionary(row):
    data_types = ["id", "major", "total", "men", "women", "category", "employed", "full_time", "part_time", "unemployed",
            "median", "p25th", "p75th", "college_jobs",  "non_college_jobs", "low_wage_jobs"]
    major = collections.OrderedDict()
    index = 0
    for cell in row:
        major[data_types[index]] = str(cell)
        if(index==9):
            if(row[9] is not None and row[2] is not None):
                major["unemployment_rate"] = str(int(row[9])/int(row[2]))
            else:
                major["unemployment_rate"] = "NULL"
        index = index + 1
    return major

def get_sort_key_percent(major, divisor):
    if(major['total'] is not None and row[divisor] is not None):
        return int(major['total'])/int(major[divisor])
    else:
        return 0

def get_url_query_string_args(category_id, minimum_salary, major_contains, sort_by, limit):
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
    arguments = {'category_id': category_id,
                 'median': minimum_salary,
                 'major_contains': major_contains,
                 'sort_by': sort_by,
                 'limit': limit}
    return arguments

def get_query_requirements(arguments):
    query_requirements = ' '
    if arguments['category_id'] != None or arguments['median'] != None or arguments['major_contains'] != None:
        query_requirements = query_requirements + 'WHERE '
    if arguments['category_id'] != None:
        query_requirements = query_requirements + 'category_id = ' + arguments['category_id'] + ' AND '
    if arguments['median'] != None:
        query_requirements = query_requirements + 'median > ' + arguments['median'] + ' AND '
    if arguments['major_contains'] != None:
        query_requirements = query_requirements + "major LIKE '%" + arguments['major_contains'].upper() + "%' AND "
    if (len(query_requirements) > 0):
        query_requirements = query_requirements[:-5] # remove extra ' AND '
    if arguments['sort_by'] != None:
        query_requirements = query_requirements + 'ORDER BY ' + arguments['sort_by']
    if arguments['limit'] != None:
        query_requirements = query_requirements + 'LIMIT ' + arguments['limit']
    print(query_requirements)

    return(query_requirements)

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
