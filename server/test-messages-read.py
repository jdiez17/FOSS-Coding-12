from euskalmap.database import db_session
from euskalmap.models import Message

# read all the messages

print " --- read ALL the messages"

for m in Message.query.all():
	print m
	
print " --- only with location data"
# read messages with location data

for m in Message.query.filter(Message.location != None):
	print m