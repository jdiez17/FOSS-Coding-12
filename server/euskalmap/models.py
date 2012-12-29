from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from euskalmap.database import Base, using_redis, r
from euskalmap.config import config
import json

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    letters = Column(String(2))
    numbers = Column(Integer)
    
    def __init__(self, letters, numbers):
        if len(letters) > 2: 
            raise Exception('Too many letters.')
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
        
        if using_redis:
            r.publish(config.get('redis', 'channel'), json.dumps(self.serialize()))
    
    def __repr__(self):
        return '<Message %r (on %r) at %r>' % (self.message, self.location, self.timestamp)
    
    def serialize(self):
        return {
                    'id': self.id,
                    'message': self.message, 
                    'location': self.location.serialize() if self.location else None, 
                    'timestamp': self.timestamp.strftime("%s") if self.timestamp else None,
                    'comments': self.comments.count()
                }        

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    message = relationship('Message', backref=backref('comments', lazy='dynamic'))
    comment = Column(Text)
    
    def __init__(self, message, text=None):
        self.message = message
        self.comment = text

    def __repr__(self):
        return '<Comment for message %r (%s)>' % (self.message.message, self.comment)
        
    def serialize(self):
        return    {
                    'id': self.id,
                    'message_id': self.message.id,
                    'comment': self.comment
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
        
    def serialize(self):
        return    {
                    'id': self.id,
                    'message': self.message.serialize(),
                    'comment': self.comment
                }