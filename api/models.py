from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from database import Base
from datetime import datetime

class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String(80), unique=True)
        password = Column(String(128))
        def __init__(self, username=None, password=None):
            self.username = username
            self.password = password

        @classmethod
        def find_by_username(cls, username):
           return cls.query.filter_by(username = username).first()    

        
class Channel(Base):
        __tablename__ = 'channels'
        id = Column(Integer, primary_key=True)
        name = Column(String(60))
        from_user = Column(Integer, ForeignKey('users.id'))
        to_user = Column(Integer, ForeignKey('users.id'))

class Message(Base):
        __tablename__ = 'messages'
        id = Column(Integer, primary_key=True)
        message = Column(Text)
        from_user = Column(Integer, ForeignKey('users.id'))
        to_user = Column(Integer, ForeignKey('users.id'))
        channel_id = Column(Integer, ForeignKey('channels.id'))
        timestamp = Column(DateTime, default=datetime.utcnow)