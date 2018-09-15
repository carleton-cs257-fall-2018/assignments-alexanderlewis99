import csv
import sys

def test_and_load():
	test_failed = False
	if(len(sys.argv) < 3):
		test_failed = True
	elif(len(sys.argv)>=3):
		action = sys.argv[2]#index
		if(not (action.lower() in ("books", "authors"))):
			test_failed = True
		if(len(sys.argv)>=4):
			sort_direction = sys.argv[3]#index
			if(not (sort_direction and (sort_direction.lower() in ("forwards", "backwards")))):
				test_failed = True
	if(test_failed):
		print("Usage: python3 books1.py input-file action [sort-direction]")
		print("action is either 'books' or 'authors'")
		print("sort-direction is either 'forwards' or 'backwards'")

	else:
		try:
			input_file = sys.argv[1]
			Lines = open(input_file, 'r')
			return Lines
		except:
			print("Error: Could not find file.")
			print("Please put it in the same folder as this file and try again.")
			return False



def get_list(reader, action):
	titleList = []
	authorList = []
	for row in reader:
		titleList.append(row[0])#adding the book name 

		indexNameEnd = str.find(row[2], "(") #finding the end of the last name
		author_full_name = row[2][0:indexNameEnd-1]
		author_last_name = author_full_name.split(" ")[-1]
		if not author_last_name in authorList:
			authorList.append(author_last_name)
	if(action=="books"):
		return sorted(titleList)
	else:
		return sorted(authorList)

def print_results(results, sort_direction):
	if(sort_direction=='forwards'):
		for i in results:
			print(i)
	else:
		for i in range(1, len(results)):
			print (results[-i])
		print (results[0])


print("=============================== books1.py V. 1.0 ===============================")
print("---------------------- by Bat-Orgil Batjargal & Alec Wang ----------------------")
Lines = test_and_load()
if(Lines):
	input_file = sys.argv[1]
	action = sys.argv[2]
	if (len(sys.argv)>=4):
		sort_direction = sys.argv[3]
	else:
		sort_direction = "fowards"
	reader = csv.reader(Lines)
	results = get_list(reader, action)
	print_results(results, sort_direction)
print("================================================================================")







#		row = row.join()
#		print(type(row))
#		if("\"" in row):
#			index = str.find(row[1,], "\"")
#			indexAuthor = str.find(row[index+2,],",")
#			title = row[1, index-1]
#		else:
#			index = str.find(row, ",")
#			indexAuthor = str.find(row[index+1,],",")
#			title = row[0,index-1]
#		full_author_name = row[indexAuthor + 1, str.find(row, "(") - 1]
#	println(title)
#	println(full_author_name)

#	titleList.append()
#	return title_list

#get_list(reader, action)



#    everyLine.append(row)
#for line in everyLine:
 # 	print (line)