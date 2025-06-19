from app import app
from models import db, Message

with app.app_context():
    Message.query.delete()

    m1 = Message(body="Hello world!", username="Ian")
    m2 = Message(body="This is a second message.", username="Jill")

    db.session.add_all([m1, m2])
    db.session.commit()