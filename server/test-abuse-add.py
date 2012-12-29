from euskalmap.database import db_session
from euskalmap.models import Message, AbuseNotice

m = Message.query.first()

items = [
            AbuseNotice(m),
            AbuseNotice(m, "Me cae mal.")
        ]

for i in items:
    db_session.add(i)
    
db_session.commit()

for an in AbuseNotice.query.all():
    print an
