import requests, shlex, sys, json
from utils import message_printer

APIBASE = "http://s.jdiez.me:5000/json/"

print "euskalMap CLI consumer - v.0.1"
print

def help(arg):
	print "Available commands: "
	print
	print ', '.join(commands.keys()) # weird python syntax. lol

	
def show(arg):
	def messages(arg):
		def print_data(url):
			data = requests.get(url)
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
				letters = arg[0][0:2]
				numbers = arg[0][3:]
				
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
	
commands = 	{
				'help': help,
				'show': show,
				'quit': quit,
			}

show(['messages', 'AK-91'])			
			
while True:
	command = shlex.split(raw_input("eM $ "))
	
	if command[0] in commands.keys():
		commands[command[0]](command[1:])
	else:
		help(None)