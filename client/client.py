import requests, shlex, sys, json
from utils import message_printer, get_location, gen_map, prettyprint_map

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
									'location': 'has_location'
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
			else:
				print "I'm sorry Bill, I'm afraid I can't let you do that."
				
	def abusenotices(msg):
		print "showing abuse notices"
		
	modes =	{
				'messages': messages,
				'abuse': abusenotices
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
		
		message = arg[0] 
		if len(arg) > 1:
			if len(arg[1]) == 5:
				letters, numbers = get_location(arg[1])
			
		payload = {'message': message, 'location_letters': letters, 'location_numbers': numbers}
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
	
commands = 	{
				'help': help,
				'show': show,
				'send': send,
				'map': map,
				'quit': quit,
			}

show(['messages', 'AK-91'])			
			
while True:
	command = shlex.split(raw_input("eM $ "))
	
	if command[0] in commands.keys():
		commands[command[0]](command[1:])
	else:
		help(None)