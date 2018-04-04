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
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,4}$', value):
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
        
        if location and category and name:
            bs = Business.query.filter(
                Business.location.ilike("%" + location + "%"),
                Business.category.ilike("%" + category + "%"),
                Business.name.ilike("%" + name + "%")
            ).paginate(page, limit, True)
            return bs

        if location and not category and not name:
            bs = Business.query.filter(
                Business.location.ilike("%" + location + "%")
            ).paginate(page, limit, True)
            return bs

        if category and not name and not location:
            bs = Business.query.filter(
                Business.category.ilike("%" + category + "%")
            ).paginate(page, limit, True)
            return bs
        if name and not location and not category:
            bs = Business.query.filter(
                Business.name.ilike("%" + name + "%")
            ).paginate(page, limit, True)
            return bs
            
        if name and category and not location:
            bs = Business.query.filter(
                Business.name.ilike("%" + name + "%"),
                Business.category.ilike("%" + category + "%")
            ).paginate(page, limit, True)
            return bs
            
        if name and location and not category:
            bs = Business.query.filter(
                Business.name.ilike("%" + name + "%"),
                Business.location.ilike("%" + location + "%")
            ).paginate(page, limit, True)
            return bs
            
        if location and  category and not name :
            bs = Business.query.filter(
                Business.category.ilike("%" + category + "%"),
                Business.location.ilike("%" + location + "%")
            ).paginate(page, limit, True)
            return bs
        
        # if no filters then return all businesses
        all = Business.query.order_by(Business.created_at.desc()).paginate(
        page, limit,True)
        return all