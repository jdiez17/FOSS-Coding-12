import datetime

def get_location(var):
	return var[0:2], var[3:]

def message_printer(data):
	def message_beautifier(message):
		out = " * [#" + str(message['id']) + "] " + "'" + message['message'] + "'"
		if message['timestamp'] != None:
			date = datetime.datetime.fromtimestamp(int(message['timestamp']))
			out += " at " + date.strftime('%Y-%m-%d %H:%M:%S')
		if message['location'] != None:
			out += " on " + message['location']['letters'] + "-" + str(message['location']['numbers'])
			
		out += ". " + str(message['comments']) + " comments."
			
		print out

	for i in data:
		message_beautifier(i)

def reports_printer(data):
	def report_beautifier(report):
		out = " * [#" + str(report['id']) + "] <Message #" + str(report['message']['id']) + " '" + report['message']['message'] + "'>"

		if report['comment'] != None:
			out += " '" + report['comment'] + "'"
		print out
		
	for report in data:
		report_beautifier(report)

def comments_printer(data):
	def comment_beautifier(comment):
		out = " * [#" + str(comment['id']) + "] " + comment['comment']
		print out
	
	for comment in data:
		comment_beautifier(comment)
		
"""
		AA1		AA2		AA3		AA4
		AB1		AB2		AB3		AB4
		AC1		AC2		AC3		AC4
		AD1		AD2		AD3		AD4
		AE1		AE2		AE3		AE4
		
		BA1		BA2		BA3		BA4
		BB1		BB2		BB3		BB4
		BC1		BC2		BC3		BC4
		BD1		BD2		BD3		BD4
		BE1		BE2		BE3		BE4
		
		This example:
		
		2 rows, 1 block per row, 5 rows per block, 4 cols per block.
		
"""

ROWS = 2
BLOCKS_PER_ROW = 5
ROWS_PER_BLOCK = 2
COLS_PER_BLOCK = 2

def prettyprint_map(map):
	c_megarow = "A"
	c_row = "A"
	
	buffer = ""
	
	for location in map:
		l_megarow = location[0][0]
		l_row = location[0][1]
		
		if l_row != c_row:
			print buffer
			buffer = ""
			c_row = l_row
			
		if l_megarow != c_megarow:
			print
			c_megarow = l_megarow	
			
		buffer += location[0] + "-" + str(location[1]) + " "
		
		count = 0 if len(location) == 2 else location[2]
		
		buffer += "(" + str(count) + ") "
		
		if location[1] % COLS_PER_BLOCK == 0:
			buffer += "  "
	print buffer
	
def gen_map():
	map = []

	for megarow in range(0, ROWS):
		for row in range(0, ROWS_PER_BLOCK):
			for col in xrange(1, COLS_PER_BLOCK*BLOCKS_PER_ROW+1):
				letters = ""
				letters += chr(ord('A') + megarow)
				letters += chr(ord('A') + row)
				
				numbers = col
				
				map.append([letters, numbers])
					
	return map