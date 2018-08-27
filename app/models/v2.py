from app import db


class TimestampMixin(object):
    """This will add created_at and updated_at timestamps to every table"""
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now()
    )


class User(TimestampMixin, db.Model):
    """model to create table users for storing user data"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    image = db.Column(db.String, default="avatar_2x.png")
    logged_in = db.Column(db.Boolean, default=False)
    businesses = db.relationship(
        'Business',
        backref='bsowner',
        cascade='all, delete-orphan'
    )
    reviews = db.relationship(
        'Review',
        backref='rvwowner',
        cascade='all, delete-orphan'
    )


class Business(TimestampMixin, db.Model):
    """ Creates business table"""
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    logo = db.Column(db.String(128), default="download_qfbj36")
    reviews = db.relationship(
        'Review',
        backref='rvwbusines',
        cascade='all, delete-orphan'
    )


class Review(TimestampMixin, db.Model):
    """ Creates Reviews table"""
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(1000))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey('businesses.id')
    )
