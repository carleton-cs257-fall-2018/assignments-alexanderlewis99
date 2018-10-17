#Alec Wang and Bat-Orgil Batjargal

#methods that we will use on the api - CareerSalaryDataSource

import re
import csv
import sys
import flask
import json
app = flask.Flask(__name__)
@app.route(/majors)
def get_majors(self, *, category_id = None, minimum_salary = None, major_search_text = None, sort_by = None, limit = None):
	if (flask.request.args.get('cat')):
		category_id = flask.request.args.get('cat')
	if (flask.request.args.get('min_sal')):
		minimum_salary  = flask.request.args.get('min_sal')
	if (flask.request.args.get('maj')):
		major_search_text = flask.request.args.get('maj')
	if (flask.request.args.get('sort'))
		sort_by = flask.request.args.get('sort')
	if (flask.request.args.get('lim')):
		limit = flask.request.args.get('lim')


	csv_file = open(recent-grads-category-ids.csv, encoding='utf-8')
    reader = csv.reader(csv_file)
    to_return = []
    
    if category_id:
        for row in reader:
            if row[6] == category_id:
            	to_return.add(row)
    if major_search_text: 
    	for item in to_return:
    		if item[2] not in major_search_text.lower():
    			to_return.remove(item)
    if minimum_salary:
    	for item in to_return:
    		if item[15] < minimum_salary
    			to_return(x)
    if to_return.len() > limit:
    	to_return = to_return[0:limit-1]

    if sort_by:
    	

    return (to_return)

    if __name__ == '__main__':



	#Get a list of all the undergraduate majors
	#try to get the data and loop and add them into a list then print

