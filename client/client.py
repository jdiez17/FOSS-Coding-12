import requests, shlex, sys, json
from utils import message_printer, get_location, gen_map, prettyprint_map, reports_printer, comments_printer

APIBASE = "http://s.jdiez.me:5000/json/"

print "euskalMap CLI consumer - v.0.1"
print

def help(arg):
	print "Available commands: "
	print
	print ', '.join(commands.keys()) # weird python syntax. lol

def request_error(code, response):
	print "! API returned code " + str(code) + " and data:"
	print response
	
def show(arg):
	def messages(arg):
		def print_data(url):
			data = requests.get(url)
			if data.status_code != 200:
				request_error(data.status_code, data.text)

			data = json.loads(data.text)
			message_printer(data)
	
		additional_arguments =	{
									'timestamp': 'has_timestamp',
									'location': 'has_location',
									'trending': 'trending'
								}
		local_args = ""
	
		base_messages = APIBASE + 'messages'
	
		if len(arg) == 0:
			print_data(base_messages)
		else:
			if len(arg[0]) == 5:
				letters, numbers = get_location(arg[0])
				
				discriminator = "/" + letters + "-" + numbers
				
				if len(arg[1:]) == 1:
					if arg[1] in additional_arguments.keys():
						local_args = "/" + additional_arguments[arg[1]]
					else:
						print "Unrecognized modifier. Available arguments: "
						print ', '.join(additional_arguments)
						return
				elif len(arg[1:]) > 1:
					print "You can't do that."
				
				
				full_url = base_messages + discriminator + local_args
				print_data(full_url)
			elif arg[0] in additional_arguments.keys():
				local_args = "/" + additional_arguments[arg[0]]
				
				full_url = base_messages + local_args
				print_data(full_url)
			
			elif arg[0] == "near":
				base_near = base_messages + "/near/"
				
				if len(arg[1]) == 5:
					letters, numbers = get_location(arg[1])
					radius = 0
					
					if len(arg) == 3:
						radius = int(arg[2])
					
					full_url = base_near + letters + "-" + numbers + ("/" + str(radius) if radius > 0 else "")
					print_data(full_url)
					
				else:
					print "You must specify a location."
				
			
			else:
				print "I'm sorry Bill, I'm afraid I can't let you do that."
				
	def abusenotices(arg):
		base_reports = APIBASE + "reports/get"
		response = requests.get(base_reports)
		if response.status_code != 200:
			return request_error(response.status_code, response.text)
		
		notices = json.loads(response.text)
		reports_printer(notices)

	modes =	{
				'messages': messages,
				'reports': abusenotices
			}
	
	if arg[0] in modes.keys():
		modes[arg[0]](arg[1:])
	else:
		print "Unrecognized item."

def quit(arg):
	sys.exit(0)
	
def send(arg):
		base_send = APIBASE + "send"

		letters = None
		numbers = 0
		timestamp = 0
		message = arg[0]
		
		if len(arg) > 1:
			if len(arg[1]) == 5:
				letters, numbers = get_location(arg[1])
				if len(arg) == 3:
					timestamp = int(arg[2])
			else:
				timestamp = int(arg[1])
				if len(arg) == 3:
					letters, numbers = get_location(arg[2])
					
		payload = {'message': message, 'location_letters': letters if letters != None else "", 'location_numbers': numbers, 'timestamp': timestamp}
		response = requests.post(base_send, data=payload)
		
		if response.status_code != 200:
			request_error(response.status_code, response.text)
			return
			
		print "Sent OK!" 

def map(arg):
	locs = gen_map()
	
	base_map = APIBASE + "messages/bulk"
	send_locations = {'locations': json.dumps(locs)}	
	response = requests.post(base_map, data=send_locations)
	
	if response.status_code != 200:
		request_error(response.status_code, response.text)
		return
		
	response = json.loads(response.text)
	for item in response:
		for i in range(0, len(locs)):
			if locs[i][0] == item['location']['letters'] and locs[i][1] == int(item['location']['numbers']):
				if len(locs[i]) == 3:
					locs[i][2] += 1
				else:
					locs[i].append(1)
				
	prettyprint_map(locs)

def report(arg):
	base_report = APIBASE + "reports/post"
	
	if int(arg[0]) == 0:
		print "You must choose a message to report."
	else:
		message = ""
		id = arg[0]
		if len(arg) == 2:
			message = arg[1]
		
		payload = {'message': message, 'id': id}
		
		response = requests.post(base_report, data=payload)
		if response.status_code != 200:
			return request_error(response.status_code, response.text)
		
		print "Abuse report received."

def comment(arg):
	base_comment = APIBASE + "comments"
	
	def post(arg):
		if len(arg) != 2:
			print "You must supply a message id and a comment."
			return
			
		base_post = base_comment + "/post"
		payload = {'id': int(arg[0]), 'comment': arg[1]}
		
		response = requests.post(base_post, data=payload)
		if response.status_code != 200:
			return request_error(response.status_code, response.text)
		
		print "Comment sent OK!"
		
	def view(arg):
		if len(arg) != 1:
			print "You must only specify the message id"
			return
		
		base_view = base_comment + "/get/"
		id = int(arg[0])
		
		response = requests.get(base_view + str(id))
		if response.status_code != 200:
			return request_error(response.status_code, response.text)
		
		data = json.loads(response.text)
		comments_printer(data)
	
	modes = 	{
					'post': post,
					'view': view
				}
	if arg[0] not in modes.keys():
		print "Unrecognized item."
		return
	modes[arg[0]](arg[1:])
	
commands = 	{
				'help': help,
				'show': show,
				'send': send,
				'map': map,
				'report': report,
				'comments': comment,
				'quit': quit,
			}
	
while True:
	command = shlex.split(raw_input("eM $ "))
	
	if command[0] in commands.keys():
		try:
			commands[command[0]](command[1:])
		except Exception, e:
			print "Exception: " + str(e)
	else:
		help(None)