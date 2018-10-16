#Alec Wang and Bat-Orgil Batjargal

#methods that we will use on the api - CareerSalaryDataSource
@app.route(/majors)
def get_majors(self, *, category = None, minimum_salary = None, major_search_text = None, sort_by = None, limit = None):
	if (flask.request.args.get('cat')):
		category = flask.request.args.get('cat')
	if (flask.request.args.get('min_sal')):
		minimum_salary  = flask.request.args.get('min_sal')
	if (flask.request.args.get('maj')):
		major_search_text = flask.request.args.get('maj')
	if (flask.request.args.get('sort'))
		sort_by = flask.request.args.get('sort')
	if (flask.request.args.get('lim')):
		limit = flask.request.args.get('lim')



	#Get a list of all the undergraduate majors
	#try to get the data and loop and add them into a list then print
