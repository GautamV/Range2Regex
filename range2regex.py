import sys

if len(sys.argv) > 3:
	print "Too many arguments!"
	sys.exit(1)

if len(sys.argv) < 3:
	print "Too few arguments!"
	sys.exit(1)

lower = list(sys.argv[1])
upper = list(sys.argv[2])

character_list = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

for c in lower: 
	if c not in character_list:
		print "Invalid character(s). Make sure all characters are between A-Z (capital) or 0-9."
		sys.exit(1)

for c in upper: 
	if c not in character_list:
		print "Invalid character(s). Make sure all characters are between A-Z (capital) or 0-9."
		sys.exit(1)


def next(c):
	if c == character_list[len(character_list)-1]:
		return c
	else: 
		return character_list[character_list.index(c) + 1]

def previous(c):
	if c == character_list[0]:
		return c
	else: 
		return character_list[character_list.index(c) - 1]

def compare(a,b):
	return character_list.index(a) - character_list.index(b)

class Range: 
	def __init__(self, start_char, end_char): 
		self.start_char = start_char
		self.end_char = end_char

	def str(self):
		return str(self.start_char) + " - " + str(self.end_char)

def adjust_range(range, start, end):
	if start and end: 
		return Range(range.start_char, range.end_char)
	elif start: 
		return Range(range.start_char, character_list[len(character_list)-1])
	elif end: 
		return Range(character_list[0], range.end_char)
	else:
		return Range(character_list[0], character_list[len(character_list)-1])

if len(upper) > len(lower):
	extras = len(upper) - len(lower)
	for num in range(0, extras):
		lower.append('*')

if len(lower) > len(upper):
	extras = len(lower) - len(upper)
	for num in range(0, extras):
		upper.append('*')

if not len(lower) == len(upper):
	print "Something weird happened - the lengths aren't the same"
	sys.exit(1)

def regexify(regex_string, range, start, end, counter):

	#print "\nregex_string is " + regex_string + ", range is " + range.str() + ", start: " + str(start) + ", end: " + str(end) + ", counter: " + str(counter) 

	if regex_string.endswith('*'):
		return regex_string

	start_star = False
	end_star = False

	if range.start_char == '*':
		ar = adjust_range(Range(character_list[0], range.end_char), start, end)
		start_star = True
	elif range.end_char == '*':
		ar = adjust_range(Range(range.start_char, character_list[len(character_list)-1]), start, end)
		end_star = True
	else:
		ar = adjust_range(range, start, end)

	if start_star and end_star:
		print "Something went wrong...the range cannot begin and end with a space."
		sys.exit(1)

	if compare(ar.start_char, ar.end_char) > 0:
		print """The range passed in doesn't make sense. The start alphabetically comes after the end."""
		sys.exit(1)

	anything = '[' + character_list[0] + '-' + character_list[len(character_list)-1] + ']*'
	pipe = '|'
	stop = '$'

	if start and end: 
		#print "\nstart and end" 
		if compare(ar.start_char, ar.end_char) <= -3:
			start_range = regex_string + ar.start_char
			mid_range = regex_string + '[' + next(ar.start_char) + '-' + previous(ar.end_char) + ']'
			end_range = regex_string + ar.end_char
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(start_range, r, True, False, counter) + pipe + regexify(mid_range, r, False, False, counter) + pipe + regexify(end_range, r, False, True, counter) + pipe + end_range + stop
				#print "\n regexify called on " + end_range
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = start_range + anything + pipe + mid_range + anything + pipe + end_range + stop
				#print "\nreturn string set to  " + return_string
			if start_star:
				return_string = regex_string + stop + pipe + return_string + stop
				#print "\nreturn string set to  " + return_string
			if end_star:
				return_string = regex_string + stop 
				#print "\nreturn string set to  " + return_string
		elif compare(ar.start_char, ar.end_char) == -2:
			start_range = regex_string + ar.start_char
			mid_range = regex_string + next(ar.start_char)
			end_range = regex_string + ar.end_char
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(start_range, r, True, False, counter) + pipe + regexify(mid_range, r, False, False, counter) + pipe + regexify(end_range, r, False, True, counter) + pipe + end_range + stop
				#print "\n regexify called on " + end_range
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = start_range + anything + pipe + mid_range + anything + pipe + end_range + stop + stop
				#print "\nreturn string set to  " + return_string
			if start_star:
				return_string = regex_string + stop + pipe + return_string + stop
				#print "\nreturn string set to  " + return_string
			if end_star:
				return_string = regex_string + stop 
				#print "\nreturn string set to  " + return_string
		elif compare(ar.start_char, ar.end_char) == -1:
			start_range = regex_string + ar.start_char
			end_range = regex_string + ar.end_char
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(start_range, r, True, False, counter) + pipe + regexify(end_range, r, False, True, counter) + pipe + end_range + stop
				#print "\n regexify called on " + end_range
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = start_range + anything + pipe + end_range + stop
				#print "\nreturn string set to  " + return_string
			if start_star:
				return_string = regex_string + stop + pipe + return_string + stop
				#print "\nreturn string set to  " + return_string
			if end_star:
				return_string = regex_string + stop 
				#print "\nreturn string set to  " + return_string
		elif compare(ar.start_char, ar.end_char) == 0:
			only_range = regex_string + ar.start_char
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(only_range, r, True, True, counter)
				#print "\n regexify called on " + only_range
				#print "\nreturn string set to  " + return_string 
			else: 
				return_string = only_range + stop
				#print "\nreturn string set to  " + return_string
			if start_star:
				return_string = regex_string + stop + pipe + return_string + stop
				#print "\nreturn string set to  " + return_string
			if end_star:
				return_string = regex_string + stop 
				#print "\nreturn string set to  " + return_string

	elif start:
		#print "\nstart only" 
		if compare(ar.start_char, ar.end_char) <= -2: 
			start_range = regex_string + ar.start_char
			mid_range = regex_string + '[' + next(ar.start_char) + '-' + ar.end_char + ']'
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(start_range, r, True, False, counter) + pipe +  regexify(mid_range, r, False, False, counter)
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = start_range + anything + pipe + mid_range + anything
				#print "\nreturn string set to  " + return_string
			if start_star:
				return_string = regex_string + stop + pipe + return_string
				#print "\nreturn string set to  " + return_string
		elif compare(ar.start_char, ar.end_char) == -1: 
			start_range = regex_string + ar.start_char
			mid_range = regex_string + next(ar.start_char)
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(start_range, r, True, False, counter) + pipe +  regexify(mid_range, r, False, False, counter)
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = start_range + anything + pipe + mid_range + anything
				#print "\nreturn string set to  " + return_string
			if start_star:
				return_string = regex_string + stop + pipe + return_string
				#print "\nreturn string set to  " + return_string
		elif compare(ar.start_char, ar.end_char) == 0: 
			only_range = regex_string + ar.start_char
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(only_range, r, True, False, counter)
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = only_range + anything 
				#print "\nreturn string set to  " + return_string
			if start_star:
				return_string = regex_string + stop + pipe + return_string
				#print "\nreturn string set to  " + return_string

	elif end: 
		#print "\nend only" 
		if compare(ar.start_char, ar.end_char) <= -2: 
			mid_range = regex_string + '[' + ar.start_char + '-' + previous(ar.end_char) + ']'
			end_range = regex_string + ar.end_char
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(mid_range, r, False, False, counter) + pipe + regexify(end_range, r, False, True, counter) + pipe + end_range + stop
				#print "\n regexify called on " + end_range
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = mid_range + anything + pipe + end_range + stop
				#print "\nreturn string set to  " + return_string
			if end_star:
				return_string = regex_string + stop 
				#print "\nreturn string set to  " + return_string
		elif compare(ar.start_char, ar.end_char) == -1:
			mid_range = regex_string + ar.start_char 
			end_range = regex_string + ar.end_char
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(mid_range, r, False, False, counter) + pipe + regexify(end_range, r, False, True, counter) + pipe + end_range + stop
				#print "\n regexify called on " + end_range
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = mid_range + anything + pipe + end_range + stop
				#print "\nreturn string set to  " + return_string
			if end_star:
				return_string = regex_string + stop 
				#print "\nreturn string set to  " + return_string
		elif compare(ar.start_char, ar.end_char) == 0:
			only_range = regex_string + ar.start_char 
			counter = counter + 1
			if counter < len(lower):
				r = Range(lower[counter], upper[counter])
				return_string = regexify(only_range, r, False, True, counter)
				#print "\n regexify called on " + only_range
				#print "\nreturn string set to  " + return_string
			else: 
				return_string = only_range + stop
				#print "\nreturn string set to  " + return_string
			if end_star:
				return_string = regex_string + stop 
				#print "\nreturn string set to  " + return_string
	else: 
		#print "\nneither start nor end" 
		#print "regex string is " + regex_string
		#print "anything is " + anything
		return_string = regex_string + anything
		#print "\nreturn string set to  " + return_string
	return return_string

initial_range = Range(lower[0], upper[0])
print regexify('^', initial_range, True, True, 0)