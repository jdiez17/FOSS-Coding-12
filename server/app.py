from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from euskalmap.database import db_session, db_unique
from euskalmap.models import Message, Location

import json

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

def output_data(format, data):
	formatters = 	{
					'json': json.dumps
					}
	
	if not format in formatters.keys():
		return "Unsupported format", 400
	
	return formatters[format](data)
	
def filter_and_output(data, filter, format):
	new_data = [i.serialize() for i in data.filter(filter)]
	
	return output_data(format, new_data)	

def get_filtered_messages(format, filter, source):
	filters = 	{
					'has_location': Message.location != None,
					'has_timestamp': Message.timestamp != None,
				}
	
	if not filter in filters.keys():
		return "Unsupported filter", 400
	
	chosen_filter = filters[filter]
	return filter_and_output(source, chosen_filter, format)
	
@app.route('/<format>/messages')
def all_messages(format):
	return filter_and_output(Message.query, None, format)
	
@app.route('/<format>/messages/<filter>')
def filtered_messages(format, filter):
	return get_filtered_messages(format, filter, Message.query)

@app.route('/<format>/messages/<letters>-<int:numbers>')
def location_messages(format, letters, numbers):
	l = db_unique(Location, letters=letters, numbers=numbers)
	return filter_and_output(l.messages, None, format)

@app.route('/<format>/messages/<letters>-<int:numbers>/<filter>')
def location_messages_filtered(format, letters, numbers, filter):
	l = db_unique(Location, letters=letters, numbers=numbers)
	return get_filtered_messages(format, filter, l.messages)
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)