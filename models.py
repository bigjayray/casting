import os
from sqlalchemy import Column, String, Integer, create_engine, Date
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "casting"
database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', database_name)
# database_path = "postgres://iogkdbxvphllfy:fe8d4ac98d57169e54886aea6b120f0ca226f903713f40f96e2c61ec8a6ac209@ec2-54-146-4-66.compute-1.amazonaws.com:5432/da3btsuh5nciev"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
# def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# TO DROP AND CREATE DATABASE 
def db_drop_and_create_all():
  db.drop_all()
  db.create_all()

'''
Movies

'''


class Movies(db.Model):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
    }


'''
Actors

'''


class Actors(db.Model):
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
    }
