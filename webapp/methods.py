#Alec Wang and Bat-Orgil Batjargal

#methods that we will use on the api - CareerSalaryDataSource
@app.route(/majors)
def get_majors():

	#Get a list of all the undergraduate majors
	#try to get the data and loop and add them into a list then print

@app.route(/majors/<category>)
def get_majors_in_catergory(<category>):

	#Get a list of all the undergraduate majors in a particular category

	limit = flask.request.args.get('limit')

@app.route(/majors/null/<program>)
def get_majors_in_program(<program>):
	limit = flask.request.args.get('limit')
	#Get a list of all the undergraduate majors in a particular program in any category

@app.route(/majors/<category>/<program>)
def get_majors_in_category_and_program(<category>, <program>):
	limit = flask.request.args.get('limit')
	sort_by_setting = flask.request.args.get('sort_by')
	#Get a list of all the undergraduate majors in a particular program in a particular category

@app.route(/majors/null/null/<minimum_salary>)
def get_majors_by_minimum_salary(<minimum_salary>):
	limit = flask.request.args.get('limit')
	#Get a list of all the undergraduate majors that make a particular minimum salary after they graduate

@app.route(majors/<category>/null/<minimum_salary>)

def get_majors_by_minimum_salary_in_category(<category>, <minimum_salary>):
	limit = flask.request.args.get('limit')

	#Get a list of all the undergraduate majors that make a particular minimum salary after they graduate in a particular category
@app.route(majors/null/<program>/<minimum_salary>)
def get_majors_by_minimum_salary_in_program(<program>, <minimum_salary>):
	limit = flask.request.args.get('limit')

	#Get a list of all the undergraduate majors that make a particular minimum salary after they graduate in a particular major from any category

@app.route(majors/<category>/<program>/<minimum_salary>)
def get_majors_by_minimum_salary_in_category_and_program(<category>,<program>,<minimum_salary>):
	limit = flask.request.args.get('limit')
	#Get a list of all the undergraduate majors that make a particular minimum salary after they graduate in a particular major from particular category
