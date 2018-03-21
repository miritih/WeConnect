from app import db

class User(db.Model):
  """model to create table users for storing user data"""
  __tablename__='users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(128))
  password = db.Column(db.String(255))
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  businesses = db.relationship('Business', backref='bsowner', cascade='all, delete-orphan')
  reviews = db.relationship('Review', backref='rvwowner', cascade='all, delete-orphan')

class Business(db.Model):
  """ Creates business table"""
  __tablename__='businesses'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  location = db.Column(db.String(255))
  category = db.Column(db.String(255))
  bio = db.Column(db.String(255))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  reviews = db.relationship('Review', backref='rvwbusines', cascade='all, delete-orphan')

class Review(db.Model):
  """ Creates Reviews table"""
  __tablename__='reviews'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))
  body = db.Column(db.String(255))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
  