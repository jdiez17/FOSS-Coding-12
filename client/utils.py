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
			
		print out

	for i in data:
		message_beautifier(i)