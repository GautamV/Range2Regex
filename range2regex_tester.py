import subprocess 
import re
from openpyxl import load_workbook

test_data = load_workbook("range2regex_test_data.xlsx", read_only=True)

ranges = test_data['Ranges']
words = test_data['Words']

all_words = set()
range_regex_dict = {}

print "Loading words..."

for row in words.rows: 
	for cell in row: 
		all_words.add(str(cell.value))
		print "Added: " + str(cell.value)

print "\nCreating Regexes..."

for row in ranges.rows:
	proc = subprocess.Popen(['python', 'range2regex.py',  row[0].value, row[1].value], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	range_regex_dict[(row[0].value, row[1].value)] = proc.communicate()[0]
	print "From Range: " + row[0].value + " - " + row[1].value 
	print "Created Regex: " +  range_regex_dict[(row[0].value, row[1].value)]

print "Testing Regexes..."
correct = True

for range in range_regex_dict:
	range_final_set = set()
	regex_final_set = set()

	for word in all_words:
		word = word.strip()
		if max(range[0], word) == word and min(range[1], word) == word:
			range_final_set.add(word)
			ran = True
		if re.match(range_regex_dict[range].strip(), word):
			regex_final_set.add(word)
			reg = True

	if not range_final_set == regex_final_set: 
		correct = False
		print "Oh no!"
		print "Set created using range " + range[0] + " - " + range[1] + " did not match set created using corresponding regex: " + range_regex_dict[range]
		print "Range's Final Set: " 
		for word in range_final_set: 
			print word
		print "Regex's Final Set: "
		for word in regex_final_set: 
			print word
		

if correct: 
	print "All regexes behaved as expected." 
	print "Test Successful!"
else:
	print "\nTest Failed."
