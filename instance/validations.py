import re
from app.models.v2 import User, Business

"""
All data validation methods will be defined in this file
"""


def validate_username(field, value, error):
    """validates if username is alredy taken"""
    username = value.strip().lower()
    if not username:
        error(field, "Field cannot be empty")
    if User.query.filter_by(username=username).first():
        error(field, "Sorry!! Username taken!")


def validate_email(field, value, error):
    """Validates the correct email and that email is not taken"""
    if User.query.filter_by(email=value).first():
        error(field, "Sorry!! Email taken!")
    if not re.match(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,4}$', value):
        error(field, "Invalid Email")


def username_taken(field, value, error):
    """ validate that duplicate usernames cannot be created"""
    username = value.strip().lower()
    if not username:
        error(field, "Field cannot be empty")
    if not User.query.filter_by(username=username).first():
        error(field, "Sorry!! Username not found!")


def validate_password(field, value, error):
    """validate password is valid and not empty"""
    if not re.match(r'\A[0-9a-zA-Z!@#$%&*]{6,20}\Z', value):
        error(
            field,
            "Password must be 6-20 Characters and can only contains leters,numbers,and any of !@#$%"
        )


def validate_bsname(field, value, error):
    """ Validate that business name cannot be duplicate"""
    name = value.strip().lower()
    if not name:
        error(field, "Business name cannot be empty")
    if Business.query.filter_by(name=name).first():
        error(field, "Sorry!! Business name taken!")


def search(filters):
    """
    Method to perform serch on businesses
    using either name location or category
    """
    category = filters["category"]
    name = filters["name"]
    location = filters["location"]
    page = filters["page"]
    limit = filters['limit']
    query = []
    if name:
      query.append(Business.name.ilike("%" + name + "%"))
    if category:
      query.append(Business.category.ilike("%" + category + "%"))
    if location:
       query.append(Business.location.ilike("%" + location + "%"))
    businesses = Business.query.filter(
        *query
    ).paginate(page, limit, True)
    
    return businesses
