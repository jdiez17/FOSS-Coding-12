from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from euskalmap.database import Base

class Location(Base):
	__tablename__ = 'locations'
	id = Column(Integer, primary_key=True)
	letters = Column(String(2))
	numbers = Column(Integer)
	
	def __init__(self, letters, numbers):
		self.letters = letters
		self.numbers = numbers
	
	def __repr__(self):
		return '<Location %s-%d>' % (self.letters, self.numbers)
		
	def serialize(self):
		return {'letters': self.letters, 'numbers': self.numbers}

class Message(Base):
	__tablename__ = 'messages'
	id = Column(Integer, primary_key=True)
	message = Column(Text)
	location_id = Column(Integer, ForeignKey('locations.id'))
	location = relationship('Location', backref=backref('messages', lazy='dynamic'))
	timestamp = Column(DateTime)

	def __init__(self, message=None, location=None, timestamp=None):
		if message == None:
			raise Exception("Needs message body.")
		self.message = message
		self.location = location
		self.timestamp = timestamp
	
	def __repr__(self):
		return '<Message %r (on %r) at %r>' % (self.message, self.location, self.timestamp)
	
	def serialize(self):
		return {
					'message': self.message, 
					'location': self.location.serialize() if self.location else None, 
					'timestamp': self.timestamp.strftime("%s") if self.timestamp else None
				}		
	
class AbuseNotice(Base):
	__tablename__ = 'abuse_notices'
	id = Column(Integer, primary_key=True)
	message_id = Column(Integer, ForeignKey('messages.id'))
	message = relationship('Message', backref=backref('reports', lazy='dynamic'))
	comment = Column(Text)
	
	def __init__(self, message, text=None):
		self.message = message
		self.comment = text

	def __repr__(self):
		return '<AbuseNotice for message %r (%s)>' % (self.message.message, self.comment)