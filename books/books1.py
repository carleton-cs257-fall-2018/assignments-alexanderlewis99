import csv
import sys

with open('books.csv', newline='') as f: #why do we need newLine= here? 
    reader = csv.reader(f)
    everyLine = []
    for row in reader:
    	wordReader = csv.reader()
        everyLine.append(row)
    for line in everyLine:
    	print (line)