from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from euskalmap.database import db_session, db_unique
from euskalmap.models import Message, Location, AbuseNotice, Comment
from euskalmap.utils import get_near, trending_order, chrono_order, random_order

from sqlalchemy import or_, and_
import json, datetime

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

def filter_and_output(data, filter, format, filter_only=False, reorder=None):
	new_data = [i.serialize() for i in data.filter(filter)]
	if reorder != None:
		new_data = reorder(new_data)
	else:
		new_data = chrono_order(new_data)
		
	return output_data(format, new_data) if not filter_only else new_data

def get_filtered_messages(format, filter, source, filter_only=False):
	filters = 	{
					'has_location': Message.location != None,
					'has_timestamp': Message.timestamp != None,
					'trending': Message.comments.any()
				}
	
	orders =	{
					'trending': trending_order,
					'random': random_order
				}
	
	if not filter in filters.keys():
		chosen_filter = None
	else:
		chosen_filter = filters[filter]
	
	order = None
	
	if filter in orders.keys():
		order = orders[filter]

	return filter_and_output(source, chosen_filter, format, filter_only, order)

def messages_by_location(format, letters, numbers, filter):
	l = db_unique(Location, letters=letters, numbers=numbers)
	return get_filtered_messages(format, filter, l.messages)

def generate_location_filter(locs):
	first = True
	for loc in locs:
		l = db_unique(Location, letters=loc[0], numbers=loc[1])
		local_filter = Message.location == l
		if first:
			filter = local_filter
			first = False
		else:
			filter = or_(filter, local_filter)	
	return filter
	
def get_messages_near(format, letters, numbers, radius=1):
	locs = get_near(letters, numbers, radius)
	filter = generate_location_filter(locs)
	
	return filter_and_output(Message.query, filter, format)
			
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
	return messages_by_location(format, letters, numbers, filter)

@app.route('/<format>/messages/bulk', methods=['POST'])
def get_bulk_messages(format):
	if "locations" not in request.form.keys():
		return "You must supply some locations.", 400
	else:
		locs = json.loads(request.form['locations'])
		filter = generate_location_filter(locs)
		return filter_and_output(Message.query, filter, format)
	
	
@app.route('/<format>/send', methods=['POST'])
def send_message(format):
	if not 'message' in request.form.keys():
		return "Missing message", 400
	else:
		message = request.form['message']
		l = None
		d = None
		
		if 'location_letters' in request.form.keys():
			if request.form['location_letters']:
				try:
					l = db_unique(Location, letters=request.form['location_letters'], numbers=int(request.form['location_numbers']))
				except Exception, e:
					return str(e), 400
		
		if 'timestamp' in request.form.keys():
			if request.form['timestamp']:
				d = datetime.datetime.fromtimestamp(int(request.form['timestamp']))
		
		try:
			m = Message(message, l, d)
			db_session.add(m)
			db_session.commit()
		except Exception, e:
			return str(e), 400
			
		return "Done."

@app.route('/<format>/messages/near/<letters>-<int:numbers>')
def messages_near(format, letters, numbers):
	return get_messages_near(format, letters, numbers, 2)

@app.route('/<format>/messages/near/<letters>-<int:numbers>/<int:radius>')
def messages_near_radius(format, letters, numbers, radius):
	return get_messages_near(format, letters, numbers, radius)
		
@app.route('/<format>/reports/post', methods=['POST'])
def add_report(format):
	id = 0
	message = ""
	
	if "id" not in request.form.keys():
		return "You must specify which message to report.", 400
	
	if "message" in request.form.keys():
		message = request.form['message']
		
	id = int(request.form['id'])

	try:
		m = Message.query.filter_by(id=id).one()
	except Exception, e:
		return str(e), 400
		
	r = AbuseNotice(m, message)
	db_session.add(r)
	
	try:
		db_session.commit()
		return "Abuse report stored."
	except:
		return "DB error", 500

@app.route('/<format>/reports/get')
def get_reports(format):
	return filter_and_output(AbuseNotice.query, None, format)

@app.route('/<format>/comments/post', methods=['POST'])
def post_comment(format):
	if not "id" in request.form.keys():
		return "You must specify the message.", 400
	if not "comment" in request.form.keys():
		return "You must specify the comment", 400
	
	id = int(request.form['id'])
	comment = request.form['comment']
	
	try:
		m = Message.query.filter_by(id=id).one()
	except Exception, e:
		return str(e), 400
	
	c = Comment(m, comment)
	db_session.add(c)
	
	try:
		db_session.commit()
	except Exception, e:
		return "DB error", 400
		
	return "Comment stored."

@app.route('/<format>/comments/get/<int:id>')
def get_comments(format, id):
	try:
		m = Message.query.filter_by(id=id).one()
	except Exception, e:
		return str(e), 400
		
	return filter_and_output(m.comments, None, format)
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)