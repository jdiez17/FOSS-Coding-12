from euskalmap.database import db_session, db_unique
from euskalmap.models import Message, Location
from datetime import datetime

for m in Message.query.all():
    db_session.delete(m)
db_session.commit()

items = [
            Message("This is a test message", db_unique(Location, letters="AK", numbers=91), datetime.now()),
            Message("Test message without location or timestamp"),
            Message("This one only has a timestamp.", None, datetime.now()),
            Message("Location, but no timestamp.", db_unique(Location, letters="AK", numbers=91))
        ]

for i in items:
    db_session.add(i)
db_session.commit()