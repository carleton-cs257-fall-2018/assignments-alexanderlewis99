# Bat-Orgil Batjargal & Alec Wang
# Sunday, September 16, 2018
# The purpose of this code is to read a CSV file with titles, dates, and
    # authors of books and return a list of either the titles or authors in
    # forward or reverse lexicographic order.
import csv
import sys

def test_and_load():
    # a function to test the terminal arguments and, if they're correct, load the file
	test_failed = False
	if(len(sys.argv) < 3):
		test_failed = True
	elif(len(sys.argv)>=3):
		action = sys.argv[2]
		if(not (action.lower() in ("books", "authors"))):
			test_failed = True
		if(len(sys.argv)>=4):
			sort_direction = sys.argv[3]
			if(not (sort_direction and (sort_direction.lower() in ("forward", "reverse")))):
				test_failed = True
	if(test_failed):
		print("Usage: python3 books1.py input-file action [sort-direction]", file=sys.stderr)
	else:
		try:
			input_file = sys.argv[1]
			books_data = open(input_file, 'r')
			return books_data
		except:
			print("Could not read file:", input_file)
			return False

def get_authors_list(reader):
	# a function to return a list of author last names without redundancies
	authorList = []
	for row in reader: 
		indexNameEnd = str.find(row[2], "(")
		author_full_name = row[2][0:indexNameEnd-1]
		author_last_name = author_full_name.split(" ")[-1]
		if not author_last_name in authorList:
			authorList.append(author_last_name)
	return sorted(authorList)

def get_titles_list(reader):
	# a function to return a list of book titles
	titleList = []
	for row in reader:
		titleList.append(row[0])
	return sorted(titleList)

def print_results(results, sort_direction):
    # prints the authors or titles in either forward or reverse lexicographic order
	if(sort_direction.lower()=='forward'):
		for i in results:
			print(i)
	else:
		for i in range(1, len(results)):
			print(results[-i])
		print(results[0])

print("=============================== books1.py V. 1.0 ===============================")
print("---------------------- by Bat-Orgil Batjargal & Alec Wang ----------------------")
books_data = test_and_load()
if(books_data):
	input_file = sys.argv[1]
	action = sys.argv[2]
	if (len(sys.argv)>=4):
		sort_direction = sys.argv[3]
	else:
		sort_direction = "forward"
	reader = csv.reader(books_data)
	if(action.lower()=="books"):
		results = get_titles_list(reader)
	else:
		results = get_authors_list(reader)
	print_results(results, sort_direction)
print("================================================================================")

