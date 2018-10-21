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

    text_to_return = ""
    text_to_return = text_to_return + 'Hello!'

    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        text_to_return + e
        exit()

    if (len(sql_query_requirements) > 0):
        sql_query = 'SELECT * FROM majors WHERE ' + sql_query_requirements
    else:
        sql_query = 'SELECT * FROM majors'
    print(sql_query)

    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)

    except Exception as e:
        print(e)
        exit()

    text_to_return = text_to_return + '===== Majors ====='

    for row in cursor:
        text_to_return = text_to_return + "{"

        for i in row:
            text_to_return = text_to_return + str(i) + ", "

        text_to_return = text_to_return + "}, "

    return(text_to_return)

    # Don't forget to close the database connection.
    connection.close()

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
                 'minimum_salary': minimum_salary,
                 'major_contains': major_contains,
                 'sort_by': sort_by,
                 'value': limit}
	return arguments

def get_query_requirements(arguments):
	query_requirements = ''
	for arg in arguments.keys():
		value = arguments[arg]
		if value != None:
			query_requirements = query_requirements + arg + ' = ' + value + ' AND '
	if (len(query_requirements) > 0):
		query_requirements = query_requirements[:-5] # remove extra ' AND '
	print(query_requirements)
	return(query_requirements)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
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
