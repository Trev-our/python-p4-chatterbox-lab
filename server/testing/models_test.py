from datetime import datetime

from app import app
from models import db, Message

class TestMessage:
    '''Message model in models.py'''

    def setup_method(self):
        '''Setup: remove any existing test messages.'''
        with app.app_context():
            m = Message.query.filter(
                Message.body == "Hello 👋"
            ).filter(Message.username == "Liza").all()

            for message in m:
                db.session.delete(message)

            db.session.commit()

    def test_has_correct_columns(self):
        '''has columns for message body, username, and creation time.'''
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert isinstance(hello_from_liza.created_at, datetime)
