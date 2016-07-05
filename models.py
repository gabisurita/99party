
import sqlalchemy as sql
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

db = sql.create_engine("sqlite:///test.db", echo=False)
#db = sql.create_engine("sqlite:///:memory:", echo=False)
Schema = declarative_base()

class Login(Schema):
  __tablename__ = "login"
  
  id = Column('id', Integer, primary_key=True)
  email = Column('email', String, unique=True)
  password = Column('password', String)
  valid = Column('valid', Boolean)
  
  
class User(Schema):
  __tablename__ = "user"
  
  id = Column('id', ForeignKey('login.id'), primary_key=True)
  login = relationship(Login)
  
  name = Column('name', String)
  cpf = Column('cpf', String(11), unique=True)
  tel = Column('tel', String)
  
  
class Business(Schema):
  __tablename__ = "business"
  id = Column('id', ForeignKey('login.id'), primary_key=True)
  login = relationship(Login)

  name = Column('name', String)
  cnpj = Column('cnpj', String(14))
  address = Column('address', String)
  tel = Column('tel', String)
  
  
class Event(Schema):
  __tablename__ = "event"
  
  creator_id = Column('creator_id', ForeignKey('business.id'))
  creator = relationship(Business)
  
  id = Column('id', Integer, primary_key=True)
  name = Column('name', String)
  date = Column('date', DateTime, default=datetime.datetime.now)
  description = Column('description', String)
  location = Column('location', String)
  picture = Column('picture', String)
  
  
class Confirmation(Schema):
  __tablename__ = "event_confirmation"
  id = Column('id', Integer, primary_key=True)
  
  eventId = Column('event_id', ForeignKey('event.id'))
  event = relationship(Event)

  userId = Column('user_id', ForeignKey('user.id'))
  user = relationship(User)
  
  checked = Column('checked', Boolean)
  

def createDB():
  Schema.metadata.create_all(db)

